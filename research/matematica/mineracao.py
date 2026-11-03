"""Bloco X: mineração de "equações" do gráfico com controle de falsas descobertas.

Biblioteca de 18 descritores matemáticos calculados de hora em hora para os 5 perpétuos
(entropia de permutação, Hurst móvel, velocidade e curvatura de Savitzky-Golay, energia
de wavelet de Haar, assimetria/curtose, compressão de range, razão de eficiência de
Kaufman, autocorrelação local, distância de máximas/mínimas, vol da vol, fração de horas
de alta, volume anormal...). Alvo: retorno das próximas 24h dividido pela volatilidade.

Procedimento sem olhar o futuro:
1. Em 2020–2023: diferença entre o decil superior e o inferior de cada descritor, t ajustado
   pela sobreposição, p-valor e seleção por Benjamini-Hochberg (taxa de falsas descobertas 10%).
2. Sinal composto = média dos postos com o sinal medido no IS, só com os aprovados.
3. Avaliação em 2024–2026 sem nenhum ajuste.
Saída: research/results/mat_mineracao.md
"""
from __future__ import annotations

import math
import sys
from itertools import permutations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter  # noqa: F401  (instalado junto com scikit-learn)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intraday"))
from core import COST, SYMS, backtest, daily, load_1m, load_funding, split_stats, table  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "mat_mineracao.md"
N = __import__("statistics").NormalDist()


def perm_entropy(x: np.ndarray, order=4) -> float:
    x = x[~np.isnan(x)]
    if len(x) < order + 10:
        return np.nan
    pats = np.array([np.argsort(x[i:i + order]) for i in range(len(x) - order + 1)])
    keys = (pats * (order ** np.arange(order))).sum(1)
    _, cnt = np.unique(keys, return_counts=True)
    p = cnt / cnt.sum()
    return float(-(p * np.log(p)).sum() / math.log(math.factorial(order)))


def haar_ratio(x: np.ndarray) -> float:
    """Energia das escalas finas / energia das escalas grossas (Haar, 64 pontos)."""
    x = x[-64:]
    if len(x) < 64 or np.isnan(x).any():
        return np.nan
    e = []
    a = x.copy()
    while len(a) >= 2:
        d = (a[0::2] - a[1::2]) / np.sqrt(2)
        a = (a[0::2] + a[1::2]) / np.sqrt(2)
        e.append((d ** 2).sum())
    e = np.array(e)
    return float(e[:2].sum() / max(e[2:].sum(), 1e-18))


def features(sym: str) -> pd.DataFrame:
    m1 = load_1m(sym)
    h = m1.resample("1h").agg({"open": "first", "high": "max", "low": "min", "close": "last",
                               "quote_volume": "sum", "taker_buy_quote": "sum"}).dropna()
    r1m = np.log(m1.close).diff()
    lr = np.log(h.close).diff()
    sig = np.sqrt((lr ** 2).ewm(halflife=24 * 7).mean())
    f = pd.DataFrame(index=h.index)
    # entropia de permutação dos últimos 60 retornos de 1 min, amostrada de hora em hora

    vals = r1m.values
    idx_pos = m1.index.searchsorted(h.index + pd.Timedelta("59min"), side="right")
    f["entropia_1m"] = [perm_entropy(vals[max(i - 120, 0):i]) for i in idx_pos]
    f["entropia_1h"] = lr.rolling(48).apply(lambda w: perm_entropy(w), raw=True)
    # Hurst local por razão de variâncias (24h sobre 1h, janela de 14 dias)
    v1 = lr.rolling(336).var()
    v24 = lr.rolling(24).sum().rolling(336).var()
    f["hurst_local"] = 0.5 + np.log((v24 / (24 * v1)).clip(lower=1e-6)) / (2 * np.log(24))
    lp = np.log(h.close)
    sm = lp.rolling(25).apply(lambda w: np.polyfit(np.arange(25), w, 2)[0], raw=True)  # curvatura (coef. quadrático)
    sl = lp.rolling(25).apply(lambda w: np.polyfit(np.arange(25), w, 1)[0], raw=True)  # velocidade
    f["curvatura"] = sm / sig
    f["velocidade"] = sl / sig
    f["wavelet_fino_grosso"] = lr.rolling(64).apply(haar_ratio, raw=True)
    f["assimetria_7d"] = lr.rolling(168).skew()
    f["curtose_7d"] = lr.rolling(168).kurt()
    rng24 = np.log(h.high.rolling(24).max() / h.low.rolling(24).min())
    f["compressao_range"] = rng24 / (sig * np.sqrt(24))
    f["eficiencia_kaufman"] = (lp - lp.shift(24)).abs() / lr.abs().rolling(24).sum()
    f["autocorr_local"] = lr.rolling(168).apply(lambda w: np.corrcoef(w[1:], w[:-1])[0, 1], raw=True)
    f["dist_max_30d"] = (lp - np.log(h.high.rolling(720).max())) / (sig * np.sqrt(24))
    f["dist_min_30d"] = (lp - np.log(h.low.rolling(720).min())) / (sig * np.sqrt(24))
    f["vol_da_vol"] = (lr.abs().rolling(24).mean()).rolling(168).std() / sig
    f["frac_horas_alta"] = (lr > 0).rolling(24).mean()
    f["volume_anormal"] = np.log(h.quote_volume / h.quote_volume.rolling(720).median())
    f["desequilibrio_agressor"] = (2 * h.taker_buy_quote / h.quote_volume - 1).rolling(24).mean()
    f["vol_relativa"] = np.log(lr.rolling(24).std() / sig)
    f["y"] = (np.log(h.close.shift(-24) / h.close) / (sig * np.sqrt(24))).clip(-8, 8)
    f["close"] = h.close
    f["sym"] = sym
    return f


def bh(p: np.ndarray, q=0.10) -> np.ndarray:
    n = len(p)
    order = np.argsort(p)
    thr = q * (np.arange(1, n + 1) / n)
    ok = p[order] <= thr
    k = np.where(ok)[0].max() + 1 if ok.any() else 0
    sel = np.zeros(n, bool)
    sel[order[:k]] = True
    return sel


def main():
    F = pd.concat([features(s) for s in SYMS])
    print("features ok", flush=True)
    feats = [c for c in F.columns if c not in ("y", "close", "sym")]
    IS = F[F.index < "2024-01-01"].dropna(subset=feats + ["y"])
    OOS = F[F.index >= "2024-01-01"]
    rows, pvals, signs = [], [], {}
    for c in feats:
        dec = pd.qcut(IS[c].rank(method="first"), 10, labels=False)
        g = IS.groupby(dec)["y"]
        top, bot = IS["y"][dec == 9], IS["y"][dec == 0]
        spread = top.mean() - bot.mean()
        se = np.sqrt(top.var() / (len(top) / 24) + bot.var() / (len(bot) / 24))
        t = spread / se
        p = 2 * (1 - N.cdf(abs(t)))
        mono = pd.Series(g.mean().values).corr(pd.Series(range(10)), method="spearman")
        # OOS com os cortes de decil do IS
        cuts = IS[c].quantile([0.1, 0.9]).values
        o_top = OOS["y"][OOS[c] > cuts[1]].dropna()
        o_bot = OOS["y"][OOS[c] < cuts[0]].dropna()
        o_spread = o_top.mean() - o_bot.mean()
        o_se = np.sqrt(o_top.var() / (len(o_top) / 24) + o_bot.var() / (len(o_bot) / 24))
        rows.append({"descritor": c, "IS: decil10 − decil1 (σ)": f"{spread:+.3f}", "IS t": round(float(t), 2),
                     "monotonia (Spearman)": round(float(mono), 2), "OOS: decil10 − decil1 (σ)": f"{o_spread:+.3f}",
                     "OOS t": round(float(o_spread / o_se), 2)})
        pvals.append(p)
        signs[c] = np.sign(spread)
    sel = bh(np.array(pvals))
    for r, s_ in zip(rows, sel):
        r["aprovado (FDR 10%)"] = "SIM" if s_ else ""
    chosen = [c for c, s_ in zip(feats, sel) if s_]
    md = ["# Resultados — Mineração de equações com controle de falsas descobertas\n",
          f"{len(feats)} descritores, alvo = retorno 24h / σ. Seleção só com 2020–2023 (Benjamini-Hochberg 10%). "
          f"Aprovados: **{', '.join(chosen) or 'nenhum'}**.\n",
          "## X1. Poder preditivo de cada descritor (IS) e o que aconteceu depois (OOS)\n", table(rows), "\n"]
    if chosen:
        port = {}
        for s in SYMS:
            d = F[F.sym == s]
            ranks = pd.DataFrame({c: d[c].rank(pct=True) * signs[c] for c in chosen})  # posto com sinal do IS
            comp = (ranks.mean(axis=1) - 0.5 * np.mean([signs[c] for c in chosen])) * 2
            # padroniza pelo IS
            sc = comp[comp.index < "2024-01-01"].std()
            pos = (comp / (2 * sc)).clip(-1, 1).rolling(24, min_periods=1).mean().fillna(0)
            bars = pd.DataFrame({"close": d.close})
            port.setdefault("composto", []).append(daily(backtest(bars, pos, COST[s], load_funding(s))).rename(s))
        rr = []
        for k, ser in port.items():
            rr += split_stats(f"Sinal composto dos descritores aprovados", pd.concat(ser, axis=1).mean(axis=1).rename(None))
        md += ["## X2. Estratégia com o sinal composto (carteira dos 5 ativos, custos + funding)\n", table(rr), "\n"]
        pd.concat(port["composto"], axis=1).mean(axis=1).to_frame("mineracao").to_parquet("/tmp/claude-0/mat_mineracao.parquet")
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
