"""Bloco Q: o que seria preciso para render 5% ao mês?

1. Monta as séries diárias das estratégias que sobreviveram fora da amostra
   (sinais de posicionamento com 1h de atraso extra, tendência+carry do estudo 1).
2. Combina com pesos de risco iguais (estimados só no período IS).
3. Calcula a alavancagem necessária para média de 5% ao mês, a alavancagem de Kelly
   e simula 10.000 trajetórias de 12 meses (bootstrap em blocos dos retornos OOS)
   com várias alavancagens: probabilidade de bater +79,6% (= 5%/mês), de perder metade
   e de ruína.
Saída: research/results/intraday_meta5.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import COST, SYMS, backtest, daily, load_funding, monthly, stats, table  # noqa: E402
from lib import DATA, btc_long  # noqa: E402
from posicionamento import hold, panel, z  # noqa: E402
from signals import trend_ensemble  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "intraday_meta5.md"
LAG, H = 1, 24
rng = np.random.default_rng(42)


def positioning_series():
    out = {"Contra o varejo": [], "Top traders × varejo": [], "Cascata de liquidação": []}
    for sym in SYMS:
        _, h = panel(sym)
        fund = load_funding(sym)
        za, zt = z(h.acc_ls).shift(LAG), z(h.top_pos_ls).shift(LAG)
        zr, zoi = z(h.close.pct_change(), 720), z(h.oi_value.pct_change(), 720).shift(LAG)
        sig = {"Contra o varejo": (za < -2, za > 2),
               "Top traders × varejo": ((zt > 1) & (za < -1), (zt < -1) & (za > 1)),
               "Cascata de liquidação": ((zr.shift(LAG) < -3) & (zoi < -2), (zr.shift(LAG) > 3) & (zoi < -2))}
        for k, (el, es) in sig.items():
            pos = hold(el.fillna(False), H) - hold(es.fillna(False), H)
            out[k].append(daily(backtest(h, pos, COST[sym], fund)).rename(sym))
    return {k: pd.concat(v, axis=1).mean(axis=1) for k, v in out.items()}


def trend_carry_btc():
    spot = pd.read_csv(DATA / "binance/spot_1d/BTCUSDT.csv", parse_dates=["date"]).set_index("date")["close"]
    perp = pd.read_csv(DATA / "binance/perp_1d/BTCUSDT.csv", parse_dates=["date"]).set_index("date")["close"]
    f = pd.read_csv(DATA / "binance/funding/BTCUSDT.csv")
    t = pd.to_datetime(f["time"], utc=True, format="mixed").dt.tz_convert(None)
    fd = pd.Series(f["rate"].values, index=t).groupby(t.dt.floor("D").values).sum()
    sig = trend_ensemble(btc_long().reindex(spot.index).ffill())
    idx = perp.index
    rs, rp = spot.pct_change().reindex(idx).fillna(0), perp.pct_change().fillna(0)
    w = sig.reindex(idx).fillna(0)
    hgt = (1 - w).shift(1).fillna(1.0)
    return rs - hgt * rp + hgt * fd.reindex(idx).fillna(0) - hgt.diff().abs().fillna(0) * 0.0008


def block_bootstrap(r: np.ndarray, n_days: int, n_paths: int, block: int = 10) -> np.ndarray:
    starts = rng.integers(0, len(r) - block, size=(n_paths, n_days // block + 1))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(n_paths, -1)[:, :n_days]
    return r[idx]


def simulate(r: pd.Series, lev: float, n_paths=10000, days=365):
    sims = block_bootstrap(r.values, days, n_paths) * lev
    sims = np.maximum(sims, -1.0)
    eq = np.cumprod(1 + sims, axis=1)
    eq = np.where(np.minimum.accumulate(eq, axis=1) <= 0.05, 0.0, eq)  # ruína: perdeu 95% (liquidação)
    final = eq[:, -1]
    dd = 1 - eq / np.maximum.accumulate(np.maximum(eq, 1e-12), axis=1)
    return {"alavancagem": f"{lev:.1f}×", "retorno 12m mediano": f"{(np.median(final) - 1)*100:+.0f}%",
            "P(≥ +79,6% = 5%/mês)": f"{(final >= 1.796).mean()*100:.0f}%",
            "P(queda ≥ 50% em algum momento)": f"{(dd.max(axis=1) >= 0.5).mean()*100:.0f}%",
            "P(ruína ≥ 95%)": f"{(final <= 0.05).mean()*100:.1f}%",
            "P(terminar no prejuízo)": f"{(final < 1).mean()*100:.0f}%"}


def main():
    S = positioning_series()
    S["Tendência + carry BTC (estudo 1)"] = trend_carry_btc()
    df = pd.DataFrame(S).dropna(how="all")
    df = df[df.index >= "2022-01-01"].fillna(0.0)  # período em que todos os sinais existem para os 5 ativos
    is_, oos = df[:"2023"], df["2024":]
    w = (1 / is_.std()) / (1 / is_.std()).sum()  # paridade de risco estimada só no IS
    df["Combinação (paridade de risco)"] = (df[list(S)] * w).sum(axis=1)
    md = ["# Resultados — A meta de 5% ao mês\n",
          f"Período comum: {df.index[0]:%Y-%m} a {df.index[-1]:%Y-%m}. Sinais de posicionamento com 1h de atraso extra. "
          f"Pesos da combinação (estimados em 2022–2023): " + ", ".join(f"{k} {v*100:.0f}%" for k, v in w.items()) + ".\n",
          "## Q1. Desempenho sem alavancagem\n"]
    rows = []
    for c in df.columns:
        for lab, sub in [("2022–2023", df[c][:"2023"]), ("OOS 2024–2026", df[c]["2024":])]:
            s = stats(sub, lab)
            rows.append({"estratégia": c, **s})
    md += [table(rows), "\n", "## Q2. Correlação entre as estratégias (diária, 2022–2026)\n",
           table([{"": i, **{k[:22]: f"{v:.2f}" for k, v in r.items()}} for i, r in df[list(S)].corr().iterrows()]), "\n"]

    md += ["## Q3. Alavancagem necessária para 5% ao mês (com base no OOS 2024–2026)\n"]
    lev_rows = []
    for c in df.columns:
        r = df[c]["2024":]
        mu, var = r.mean(), r.var()
        m_mean = monthly(r).mean()
        kelly = mu / var if var > 0 else np.nan
        lev_rows.append({"estratégia": c, "média/mês 1×": f"{m_mean*100:+.2f}%",
                         "alavancagem p/ 5%/mês (aritmético)": f"{0.05/m_mean:.1f}×" if m_mean > 0 else "impossível",
                         "Kelly (ótimo teórico)": f"{kelly:.1f}×", "½ Kelly (usual)": f"{kelly/2:.1f}×"})
    md += [table(lev_rows), "\n",
           "Acima do Kelly, mais alavancagem **reduz** o crescimento esperado e aumenta a chance de ruína.\n",
           "## Q4. Monte Carlo — 10.000 trajetórias de 12 meses (bootstrap em blocos de 10 dias dos retornos OOS 2024–2026)\n"]
    for c in ["Combinação (paridade de risco)", "Contra o varejo", "Tendência + carry BTC (estudo 1)"]:
        r = df[c]["2024":]
        m_mean = monthly(r).mean()
        levs = sorted({1.0, 2.0, 3.0, 5.0, round(0.05 / m_mean, 1) if m_mean > 0 else 1.0})
        md += [f"### {c}\n", table([simulate(r, L) for L in levs]), "\n"]
    OUT.write_text("\n".join(md))
    df.to_parquet("/tmp/claude-0/meta5_series.parquet")
    print("\n".join(md))


if __name__ == "__main__":
    main()
