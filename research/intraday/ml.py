"""Bloco P: aprendizado de máquina (LightGBM) com walk-forward mensal.

Painel horário dos 5 perpétuos com variáveis de preço, volatilidade, posicionamento
(varejo e top traders), fluxo agressor, open interest, funding e calendário.
Alvo: retorno das próximas 24h dividido pela volatilidade. Um único modelo para os 5 ativos.
Treino expansivo até o mês anterior (com 24h de "purga" para não vazar o alvo) e previsão do mês seguinte.
Posição = previsão padronizada, limitada a ±1, aplicada hora a hora com custos e funding.
Todas as previsões são fora da amostra. Saída: research/results/intraday_ml.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import COST, SYMS, backtest, daily, load_funding, split_stats, table  # noqa: E402
from posicionamento import panel, z  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "intraday_ml.md"
DATA_CACHE = Path("/tmp/claude-0/ml_panel.parquet")


def features(h: pd.DataFrame, fund: pd.Series, btc: pd.DataFrame | None) -> pd.DataFrame:
    f = pd.DataFrame(index=h.index)
    lr = np.log(h.close).diff()
    for k in (1, 4, 24, 72, 168):
        f[f"r_{k}"] = np.log(h.close / h.close.shift(k))
    f["vol_24"] = lr.rolling(24).std()
    f["vol_ratio"] = f["vol_24"] / lr.rolling(168).std()
    f["z_acc"] = z(h.acc_ls)
    f["z_top"] = z(h.top_pos_ls)
    f["acc_lvl"] = h.acc_ls
    f["top_lvl"] = h.top_pos_ls
    f["d_acc_24"] = h.acc_ls.pct_change(24)
    f["d_top_24"] = h.top_pos_ls.pct_change(24)
    f["taker"] = np.log(h.taker_ratio.replace(0, np.nan))
    f["z_taker"] = z(f["taker"])
    f["d_oi_1"] = z(h.oi_value.pct_change(), 720)
    f["d_oi_24"] = h.oi_value.pct_change(24)
    fh = fund.reindex(h.index, method="ffill")
    f["funding"] = fh
    f["z_funding"] = z(fh, 24 * 30)
    f["hour_sin"], f["hour_cos"] = np.sin(2 * np.pi * h.index.hour / 24), np.cos(2 * np.pi * h.index.hour / 24)
    f["dow"] = h.index.dayofweek
    if btc is not None:
        f["btc_r_24"] = np.log(btc.close / btc.close.shift(24)).reindex(h.index)
        f["btc_z_acc"] = z(btc.acc_ls).reindex(h.index)
    else:
        f["btc_r_24"] = f["r_24"]
        f["btc_z_acc"] = f["z_acc"]
    f["target"] = np.log(h.close.shift(-24) / h.close) / f["vol_24"].replace(0, np.nan) / np.sqrt(24)
    return f


def build():
    if DATA_CACHE.exists():
        return pd.read_parquet(DATA_CACHE)
    hs = {s: panel(s)[1] for s in SYMS}
    frames = []
    for s, h in hs.items():
        f = features(h, load_funding(s), hs["BTCUSDT"] if s != "BTCUSDT" else None)
        f["sym"] = s
        f["close"] = h.close
        frames.append(f)
    df = pd.concat(frames)
    df.to_parquet(DATA_CACHE)
    return df


def main():
    df = build()
    feats = [c for c in df.columns if c not in ("target", "sym", "close")]
    df["sym_id"] = df["sym"].astype("category").cat.codes
    feats.append("sym_id")
    months = pd.period_range("2022-06", df.index.max().to_period("M"), freq="M")
    preds = []
    imp = pd.Series(0.0, index=feats)
    for m in months:
        start = m.to_timestamp()
        end = (m + 1).to_timestamp()
        tr = df[(df.index < start - pd.Timedelta("24h"))].dropna(subset=["target"])
        te = df[(df.index >= start) & (df.index < end)]
        if len(tr) < 20000 or te.empty:
            continue
        model = lgb.LGBMRegressor(n_estimators=300, learning_rate=0.03, num_leaves=15, min_child_samples=300,
                                  subsample=0.8, subsample_freq=1, colsample_bytree=0.8, reg_lambda=5.0, verbose=-1)
        model.fit(tr[feats], tr["target"].clip(-5, 5))
        p = pd.Series(model.predict(te[feats]), index=te.index)
        scale = pd.Series(model.predict(tr[feats].iloc[-24 * 90 * 5:])).std()
        preds.append(pd.DataFrame({"sym": te["sym"].values, "pred": (p / scale).values, "target": te["target"].values,
                                   "close": te["close"].values}, index=te.index))
        imp += pd.Series(model.booster_.feature_importance("gain"), index=feats)
        print(m, len(tr), flush=True)
    P = pd.concat(preds)
    ic = P.groupby(P.index.to_period("M")).apply(lambda g: g["pred"].corr(g["target"], method="spearman"))
    rows, port = [], {}
    for thr_name, f in [("posição = previsão (±1)", lambda x: x.clip(-1, 1)),
                        ("só sinais fortes (|z|>1)", lambda x: np.sign(x).where(x.abs() > 1, 0.0))]:
        for sym in SYMS:
            g = P[P.sym == sym]
            b = pd.DataFrame({"close": g["close"]})
            pos = f(g["pred"]).rolling(24, min_periods=1).mean()  # 24 tranches: suaviza giro
            r = backtest(b, pos, COST[sym], load_funding(sym))
            port.setdefault(thr_name, []).append(daily(r).rename(sym))
    for name, series in port.items():
        d = pd.concat(series, axis=1).mean(axis=1)
        rows += split_stats(f"LightGBM · {name}", d.rename(None), is_end="2023-12-31", oos_start="2024-01-01",
                            labels=("2022-06–2023 (fora da amostra)", "2024–2026 (fora da amostra)"))
    md = ["# Resultados — Machine learning (LightGBM, walk-forward mensal)\n",
          f"{len(feats)} variáveis, {len(P):,} previsões horárias fora da amostra (jun/2022–out/2026), 5 ativos.\n",
          f"Correlação de postos (IC) média entre previsão e retorno 24h: **{ic.mean():.3f}** "
          f"(meses com IC > 0: {(ic > 0).mean()*100:.0f}%).\n",
          table(rows), "\n", "## Importância das variáveis (ganho acumulado)\n",
          table([{"variável": k, "importância_%": f"{v/imp.sum()*100:.1f}%"} for k, v in imp.sort_values(ascending=False).head(15).items()]), "\n"]
    OUT.write_text("\n".join(md))
    P.to_parquet("/tmp/claude-0/ml_preds.parquet")
    print("\n".join(md))


if __name__ == "__main__":
    main()
