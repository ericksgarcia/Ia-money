"""Reteste dos pares de Kalman com ruído de medição mais sensível (ve = 1e-4 em log-preço).
Saída: research/results/mat_kalman.md"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intraday"))
import statarb as sa  # noqa: E402
from core import split_stats, table  # noqa: E402

rows = []
P = sa.panel()
R = np.log(P).diff().fillna(0.0)
Fh = sa.funding_hourly(P.index)
for ve in (1e-3, 1e-4):
    for a, b in [("ETHUSDT", "BTCUSDT"), ("SOLUSDT", "ETHUSDT"), ("XRPUSDT", "DOGEUSDT")]:
        z, beta = sa.kalman_pair(P[a], P[b], delta=1e-5, ve=ve)
        st = pd.Series(np.nan, index=P.index)
        st[z > 2] = -1.0
        st[z < -2] = 1.0
        st[(np.sign(z) != np.sign(z.shift(1))) & st.isna()] = 0.0
        st = st.ffill().fillna(0.0)
        st.iloc[:720] = 0.0
        N = pd.DataFrame(0.0, index=P.index, columns=P.columns)
        N[a] = st * 0.5
        N[b] = -st * beta.clip(0, 3) * 0.5
        trades = float((st.diff().abs() > 0).sum() / (len(st) / 24))
        rows += split_stats(f"Kalman {a[:-4]}/{b[:-4]} · ve={ve:g}", sa.run_portfolio(N, R, Fh), extra={"trocas/dia": round(trades, 2)})
out = Path(__file__).resolve().parents[1] / "results" / "mat_kalman.md"
out.write_text("# Resultados — Pares com filtro de Kalman (dois níveis de sensibilidade)\n\n" + table(rows) + "\n")
print(table(rows))
