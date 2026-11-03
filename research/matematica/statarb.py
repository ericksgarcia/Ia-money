"""Bloco U: arbitragem estatística — o preço relativo como processo de Ornstein-Uhlenbeck.

U1. Avellaneda & Lee (2010): a cada hora, PCA dos retornos dos 5 perpétuos (janela de 30
    dias) → fator de mercado; resíduo de cada ativo acumulado = X_t; ajuste AR(1)/OU
    (κ, m, σ_eq) → s-score. Abre vendido em s > 1,25, comprado em s < −1,25, fecha em
    |s| < 0,5, com hedge do fator. Só opera se a meia-vida for < 5 dias.
U2. Pares com filtro de Kalman (β dinâmico): ETH/BTC, SOL/ETH, XRP/DOGE.
    Entra em |z| > 2, sai quando z cruza 0.
Custos por perna (taker + slippage) e funding real. Saída: research/results/mat_statarb.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intraday"))
from core import COST, SYMS, daily, load_1m, load_funding, split_stats, table  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "mat_statarb.md"


def panel():
    P = {}
    for s in SYMS:
        m1 = load_1m(s)
        P[s] = m1.close.resample("1h").last()
    P = pd.DataFrame(P).dropna()
    return P


def funding_hourly(idx):
    F = {}
    for s in SYMS:
        f = load_funding(s)
        loc = idx.searchsorted(f.index, side="right") - 1
        arr = np.zeros(len(idx))
        ok = (loc >= 0) & (loc < len(idx))
        np.add.at(arr, loc[ok], f.values[ok])
        F[s] = arr
    return pd.DataFrame(F, index=idx)


def run_portfolio(N: pd.DataFrame, R: pd.DataFrame, Fh: pd.DataFrame) -> pd.Series:
    held = N.shift(1).fillna(0)
    cost = pd.Series(COST)[N.columns]
    turn = N.diff().abs().fillna(N.abs())
    r = (held * R).sum(axis=1) - (turn * cost).sum(axis=1) - (held * Fh).sum(axis=1)
    return r


def avellaneda_lee(P: pd.DataFrame, W=720, entry=1.25, exit_=0.5, max_hl=120):
    R = np.log(P).diff().fillna(0.0)
    Rv = R.values
    T, n = Rv.shape
    S = np.full((T, n), np.nan)
    B = np.zeros((T, n))
    Wf = np.zeros((T, n))
    for t in range(W, T):
        x = Rv[t - W:t]
        sd = x.std(axis=0) + 1e-12
        zc = (x - x.mean(axis=0)) / sd
        _, vecs = np.linalg.eigh(np.cov(zc.T))
        v = vecs[:, -1]
        w = v / sd
        w = w / np.abs(w).sum()
        f = x @ w
        beta = ((x - x.mean(0)) * (f - f.mean())[:, None]).sum(0) / ((f - f.mean()) ** 2).sum()
        eps = x - np.outer(f, beta)
        X = np.cumsum(eps, axis=0)
        x0, x1 = X[:-1], X[1:]
        for i in range(n):
            b, a = np.polyfit(x0[:, i], x1[:, i], 1)
            if not (0 < b < 1):
                continue
            kappa = -np.log(b)
            if 1 / kappa > max_hl:
                continue
            m = a / (1 - b)
            res = x1[:, i] - (a + b * x0[:, i])
            seq = np.sqrt(res.var() / (1 - b * b))
            S[t, i] = (X[-1, i] - m) / seq
        B[t] = beta
        Wf[t] = w
    S = pd.DataFrame(S, index=P.index, columns=P.columns)
    pos = pd.DataFrame(0.0, index=P.index, columns=P.columns)
    cur = np.zeros(n)
    Sv = S.values
    for t in range(T):
        for i in range(n):
            s = Sv[t, i]
            if np.isnan(s):
                cur[i] = 0.0
            elif cur[i] == 0:
                cur[i] = -1.0 if s > entry else (1.0 if s < -entry else 0.0)
            elif cur[i] == 1 and s > -exit_:
                cur[i] = 0.0
            elif cur[i] == -1 and s < exit_:
                cur[i] = 0.0
        pos.iloc[t] = cur
    # posição líquida: ativo i ± hedge β_i × carteira do fator
    N = pos.copy() * 0.0
    for t in range(T):
        p = pos.values[t]
        if not p.any():
            continue
        net = p.copy()
        hedge = (p * B[t]).sum()
        net = net - hedge * Wf[t]
        N.iloc[t] = net / max(np.abs(net).sum(), 1.0) * min(np.abs(p).sum(), n) / n
    return N, R


def kalman_pair(y: pd.Series, x: pd.Series, delta=1e-5, ve=1e-3):
    yv, xv = np.log(y.values), np.log(x.values)
    n = len(yv)
    theta = np.zeros(2)
    Pm = np.eye(2)
    Vw = delta / (1 - delta) * np.eye(2)
    z = np.full(n, np.nan)
    beta = np.zeros(n)
    for t in range(n):
        F = np.array([1.0, xv[t]])
        Pm = Pm + Vw
        yhat = F @ theta
        Q = F @ Pm @ F + ve
        e = yv[t] - yhat
        z[t] = e / np.sqrt(Q)
        K = Pm @ F / Q
        theta = theta + K * e
        Pm = Pm - np.outer(K, F) @ Pm
        beta[t] = theta[1]
    return pd.Series(z, index=y.index), pd.Series(beta, index=y.index)


def main():
    P = panel()
    R = np.log(P).diff().fillna(0.0)
    Fh = funding_hourly(P.index)
    md = ["# Resultados — Arbitragem estatística (Ornstein-Uhlenbeck, PCA, Kalman)\n",
          f"Painel horário {P.index[0]:%Y-%m} → {P.index[-1]:%Y-%m}, 5 perpétuos.\n"]
    rows = []
    for W, ent in [(720, 1.25), (720, 2.0), (24 * 60, 1.5)]:
        N, _ = avellaneda_lee(P, W=W, entry=ent)
        r = run_portfolio(N, R, Fh)
        rows += split_stats(f"PCA/OU (janela {W//24}d, entrada |s|>{ent})", r)
        print("AL", W, ent, flush=True)
    for a, b in [("ETHUSDT", "BTCUSDT"), ("SOLUSDT", "ETHUSDT"), ("XRPUSDT", "DOGEUSDT")]:
        z, beta = kalman_pair(P[a], P[b])
        st = pd.Series(np.nan, index=P.index)
        st[z > 2] = -1.0
        st[z < -2] = 1.0
        cross = np.sign(z) != np.sign(z.shift(1))
        st[cross & st.isna()] = 0.0
        st = st.ffill().fillna(0.0)
        st.iloc[:24 * 30] = 0.0
        N = pd.DataFrame(0.0, index=P.index, columns=P.columns)
        N[a] = st * 0.5
        N[b] = -st * beta.clip(0, 3) * 0.5
        r = run_portfolio(N, R, Fh)
        rows += split_stats(f"Par Kalman {a[:-4]}/{b[:-4]}", r)
    md += [table(rows), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
