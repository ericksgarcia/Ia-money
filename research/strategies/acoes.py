"""Estudo de estratégias em AÇÕES (EUA 1926–2026 e Brasil 2001–2026).

Blocos
 A. Fatores fundamentalistas/quantitativos long-short (Fama-French, EUA)
 B. Timing do mercado EUA (mensal): tendência, momentum de série temporal,
    valuation (CAPE), sazonalidade — long/flat e long/short
 C. Regras técnicas diárias no mercado EUA (MM200, cruzamento 50/200,
    RSI(2), Donchian, virada de mês)
 D. Brasil (NEFIN): fatores long-short e timing do mercado com CDI como caixa

Saída: research/results/acoes.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import (fmt_table, ff_daily, ff_monthly, nefin_daily, perf, rsi,  # noqa: E402
                 run_signal, shiller, sma)

OUT = Path(__file__).resolve().parents[1] / "results" / "acoes.md"
TRIALS = 60  # nº aproximado de variantes testadas neste arquivo (para o DSR)
md: list[str] = ["# Resultados — Ações\n", "Gerado por `research/strategies/acoes.py`. "
                 "Sharpe sobre o caixa (T-bill nos EUA, CDI no Brasil); fatores long-short são autofinanciados. "
                 f"DSR = Sharpe deflacionado considerando ~{TRIALS} tentativas (prob. de o Sharpe real ser > 0).\n"]


def capm_alpha(r: pd.Series, mkt_rf: pd.Series, ppy: int) -> tuple[float, float]:
    d = pd.concat([r, mkt_rf], axis=1, sort=True).dropna()
    y, x = d.iloc[:, 0].values, d.iloc[:, 1].values
    X = np.column_stack([np.ones_like(x), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ b
    s2 = resid.var(ddof=2)
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[0, 0])
    return b[0] * ppy, b[0] / se


# =============================================================== A. fatores EUA
ff = ff_monthly()
PUB = {"SMB": 1981, "HML": 1992, "RMW": 2013, "CMA": 2015, "UMD": 1993,
       "STR": 1990, "LTR": 1985, "LOWBETA": 2006, "LOWVOL": 2006}
NOME = {"SMB": "Tamanho (small − big)", "HML": "Valor (P/VPA baixo − alto)",
        "RMW": "Qualidade/rentabilidade", "CMA": "Investimento conservador",
        "UMD": "Momentum 12-1 meses", "STR": "Reversão curto prazo (1m)",
        "LTR": "Reversão longo prazo (3-5a)", "LOWBETA": "Beta baixo − alto",
        "LOWVOL": "Volatilidade baixa − alta"}
# giro mensal aproximado (fração do portfólio negociada por mês, por perna)
GIRO = {"SMB": 0.03, "HML": 0.04, "RMW": 0.04, "CMA": 0.04, "UMD": 0.30,
        "STR": 0.90, "LTR": 0.05, "LOWBETA": 0.06, "LOWVOL": 0.06}
CUSTO_TRADE = 0.0020  # 0,20% por operação (spread+corretagem+impacto), estimativa

rows = []
for f, nome in NOME.items():
    r = ff[f].dropna()
    custo_aa = 12 * 2 * GIRO[f] * CUSTO_TRADE
    for label, sub in [("completo", r), (f"pós-{PUB[f]}", r[r.index.year > PUB[f]]),
                       ("2010–2025", r[r.index.year >= 2010])]:
        p = perf(sub, 12, trials=TRIALS)
        a, t = capm_alpha(sub, ff["MKT_RF"], 12)
        rows.append({"fator": nome, "período": label, "inicio": p["inicio"], "fim": p["fim"],
                     "media": sub.mean() * 12, "vol": p["vol"], "sharpe": p["sharpe"], "t": p["t"],
                     "alfa_CAPM": f"{a*100:.1f}% (t={t:.1f})", "maxDD": p["maxDD"],
                     "custo_est_aa": f"{custo_aa*100:.1f}%"})
md += ["## A. Fatores long-short nos EUA (Fama-French, retornos brutos)\n",
       fmt_table(rows, ["fator", "período", "inicio", "fim", "media", "vol", "sharpe", "t", "alfa_CAPM", "maxDD", "custo_est_aa"]),
       "\n`custo_est_aa` = 12 × 2 pernas × giro mensal típico × 0,20% — estimativa simples; fatores de alto giro "
       "(reversão de 1 mês, momentum) perdem boa parte do prêmio na prática.\n"]

# =============================================================== B. timing mensal EUA
mkt, rf = ff["MKT"], ff["RF"]
idx = (1 + mkt).cumprod()
sh = shiller()
cape = sh["PE10"].reindex(mkt.index, method="ffill").shift(1)  # lucro chega com atraso
cape_all = sh["PE10"].dropna()
pct = pd.Series(index=mkt.index, dtype=float)
for d in mkt.index:
    hist = cape_all[cape_all.index < d]
    if len(hist) >= 240 and not np.isnan(cape.get(d, np.nan)):
        pct[d] = (hist < cape[d]).mean()

C_ETF = 0.001
strategies = {
    "Buy & hold": pd.Series(1.0, index=mkt.index),
    "MM 10 meses (long/caixa)": (idx > sma(idx, 10)).astype(float),
    "MM 10 meses (long/short)": np.where(idx > sma(idx, 10), 1.0, -1.0),
    "Momentum 12m (long/caixa)": ((idx / idx.shift(12) - 1) > (1 + rf).rolling(12).apply(np.prod, raw=True) - 1).astype(float),
    "Momentum 12m (long/short)": np.where((idx / idx.shift(12) - 1) > (1 + rf).rolling(12).apply(np.prod, raw=True) - 1, 1.0, -1.0),
    "CAPE: peso = 1 − percentil": (1 - pct).clip(0, 1),
    "CAPE: sai se percentil > 90%": (pct <= 0.9).astype(float).where(pct.notna()),
    "Sazonal: nov–abr dentro, mai–out caixa": pd.Series(np.where(mkt.index.month.isin([11, 12, 1, 2, 3, 4]), 1.0, 0.0), index=mkt.index).shift(-1),
}
rows = []
start = pd.Timestamp("1927-12-31")
for name, pos in strategies.items():
    pos = pd.Series(pos, index=mkt.index)
    r = run_signal(mkt, pos, C_ETF, cash=rf)[start:]
    held = pos.shift(1).reindex(r.index)
    for label, sub in [("1928–2026", r), ("IS 1928–1989", r[:"1989"]), ("OOS 1990–2026", r["1990":])]:
        p = perf(sub, 12, rf=rf, trials=TRIALS)
        rows.append({"estratégia": name, "período": label, "CAGR": p["CAGR"], "vol": p["vol"],
                     "sharpe": p["sharpe"], "maxDD": p["maxDD"], "calmar": p["calmar"],
                     "exposicao": float(held.reindex(sub.index).abs().mean()), "DSR": p["DSR"]})
md += ["## B. Timing do mercado EUA (mensal, total return, caixa = T-bill, custo 0,10%/troca)\n",
       fmt_table(rows), "\n"]

# =============================================================== C. regras diárias EUA
fd = ff_daily()
dm, drf = fd["MKT"], fd["RF"]
didx = (1 + dm).cumprod()
C_D = 0.0005
r2 = rsi(didx, 2)
pos_rsi = pd.Series(np.nan, index=didx.index)
pos_rsi[(r2 < 10) & (didx > sma(didx, 200))] = 1.0
pos_rsi[didx > sma(didx, 5)] = 0.0
pos_rsi = pos_rsi.ffill().fillna(0.0)
hi55, lo20 = didx.rolling(55).max(), didx.rolling(20).min()
pos_don = pd.Series(np.nan, index=didx.index)
pos_don[didx >= hi55] = 1.0
pos_don[didx <= lo20] = 0.0
pos_don = pos_don.ffill().fillna(0.0)
# virada de mês: último pregão do mês + 3 primeiros pregões (sinal definido em t-1)
ym = didx.index.to_period("M")
rank_fwd = pd.Series(1, index=didx.index).groupby(ym).cumsum()
n_in_month = pd.Series(1, index=didx.index).groupby(ym).transform("sum")
is_tom_day = (rank_fwd <= 3) | (rank_fwd == n_in_month)
pos_tom = is_tom_day.astype(float).shift(-1).fillna(0.0)  # posição decidida na véspera
daily = {
    "Buy & hold": pd.Series(1.0, index=didx.index),
    "MM200 (long/caixa)": (didx > sma(didx, 200)).astype(float),
    "Cruzamento MM50/MM200": (sma(didx, 50) > sma(didx, 200)).astype(float),
    "Donchian 55/20 (rompimento)": pos_don,
    "RSI(2)<10 acima da MM200 (reversão)": pos_rsi,
    "Virada de mês (4 pregões)": pos_tom,
}
rows = []
for name, pos in daily.items():
    r = run_signal(dm, pos, C_D, cash=drf)["1927":]
    held = pos.shift(1).reindex(r.index)
    for label, sub in [("1927–2021", r), ("IS 1927–1989", r[:"1989"]), ("OOS 1990–2021", r["1990":])]:
        p = perf(sub, 252, rf=drf, trials=TRIALS)
        trades = float(held.reindex(sub.index).diff().abs().sum() / p["anos"] / 2)
        rows.append({"estratégia": name, "período": label, "CAGR": p["CAGR"], "vol": p["vol"],
                     "sharpe": p["sharpe"], "maxDD": p["maxDD"], "exposicao": float(held.reindex(sub.index).mean()),
                     "trades_ano": round(trades, 1), "DSR": p["DSR"]})
md += ["## C. Regras técnicas diárias — mercado EUA (1927–2021, custo 0,05%/lado, caixa = T-bill)\n",
       fmt_table(rows), "\n"]

# =============================================================== D. Brasil (NEFIN)
nf = nefin_daily()
rows = []
NOME_BR = {"MKT_RF": "Mercado − CDI", "SMB": "Tamanho", "HML": "Valor", "WML": "Momentum", "IML": "Iliquidez"}
for f, nome in NOME_BR.items():
    r = nf[f].dropna()
    for label, sub in [("2001–2026", r), ("2001–2013", r[:"2013"]), ("2014–2026", r["2014":])]:
        p = perf(sub, 252, trials=TRIALS)
        rows.append({"fator": nome, "período": label, "media": sub.mean() * 252, "vol": p["vol"],
                     "sharpe": p["sharpe"], "t": p["t"], "maxDD": p["maxDD"], "DSR": p["DSR"]})
md += ["## D1. Brasil — fatores long-short (NEFIN-USP, diário)\n", fmt_table(rows), "\n"]

bm, brf = nf["MKT"], nf["RF"]
bidx = (1 + bm).cumprod()
br = {
    "Buy & hold (índice NEFIN)": pd.Series(1.0, index=bidx.index),
    "CDI puro": pd.Series(0.0, index=bidx.index),
    "MM200 (long/CDI)": (bidx > sma(bidx, 200)).astype(float),
    "Momentum 12m vs CDI (long/CDI)": ((bidx / bidx.shift(252)) > (1 + brf).rolling(252).apply(np.prod, raw=True)).astype(float),
    "Momentum 12m (long/short)": np.where((bidx / bidx.shift(252)) > (1 + brf).rolling(252).apply(np.prod, raw=True), 1.0, -1.0),
}
rows = []
for name, pos in br.items():
    pos = pd.Series(pos, index=bidx.index)
    r = run_signal(bm, pos, C_D, cash=brf)["2002":]
    for label, sub in [("2002–2026", r), ("2002–2013", r[:"2013"]), ("2014–2026", r["2014":])]:
        p = perf(sub, 252, rf=brf, trials=TRIALS)
        rows.append({"estratégia": name, "período": label, "CAGR": p["CAGR"], "vol": p["vol"],
                     "sharpe": p["sharpe"], "maxDD": p["maxDD"], "DSR": p["DSR"]})
md += ["## D2. Brasil — timing do mercado com CDI como caixa (custo 0,05%/lado)\n", fmt_table(rows), "\n"]

OUT.write_text("\n".join(md))
print("\n".join(md))
