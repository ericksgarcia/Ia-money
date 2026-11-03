"""Bloco N: day trade em ações — SPY 1 minuto (2008–2021, GitHub CryonicArtist/Xlchedelic).

N1. ORB de 5 minutos (Zarattini & Aziz 2023, "Can Day Trading Really Be Profitable?"),
    com e sem o dimensionamento do artigo (arrisca 1% por trade, alavancagem até 4×).
    O artigo usou 2016–2023; aqui 2008–2015 é um teste FORA da amostra do artigo.
N2. Momentum da "zona de ruído" (Zarattini, Aziz & Barbon 2024, "Beat the Market"),
    1× e com volatilidade-alvo de 2% ao dia (até 4×).
N3. Momentum intradiário (Gao, Han, Li & Zhou 2018): retorno da 1ª meia hora prevê a última.
N4. Fade de gap de abertura.
N5. Overnight × intradiário (de onde vem o retorno do SPY).
N6. Setups populares em 5 min (MME 9/21, RSI 30/70, VWAP) e seus fades, só intradiário.

Custos por lado: 1 pb (conservador para varejo; spread do SPY ≈ 0,25 pb) e 0,25 pb (otimista).
IS = 2008–2015, OOS = 2016–2021.
Saída: research/results/intraday_spy.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import INTRA, backtest, ema, rsi, split_stats, state, table  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "intraday_spy.md"
KW = dict(ppy=252, is_end="2015-12-31", oos_start="2016-01-01", labels=("IS 2008–2015", "OOS 2016–2021"))


def load():
    s = pd.read_parquet(INTRA / "SPY_1m.parquet")
    t = pd.to_datetime(s.pop("date"))
    s.index = t
    m = t.dt.hour * 60 + t.dt.minute
    reg = s[((m >= 450) & (m <= 839)).values].copy()  # 07:30–13:59 (horário ET−2) = 9:30–15:59 ET
    reg["k"] = (reg.index.hour * 60 + reg.index.minute - 450).values
    reg["d"] = reg.index.normalize()
    piv = {c: reg.pivot_table(index="d", columns="k", values=c, aggfunc="last") for c in ["open", "high", "low", "close", "volume"]}
    C = piv["close"].ffill(axis=1)
    O = piv["open"].fillna(C)
    H = piv["high"].fillna(C)
    L = piv["low"].fillna(C)
    V = piv["volume"].fillna(0)
    ok = C.notna().sum(axis=1) >= 380
    return reg, O[ok], H[ok], L[ok], C[ok], V[ok]


def to_series(x, idx):
    return pd.Series(np.asarray(x, dtype=float), index=idx).fillna(0.0)


def orb(O, H, L, C, cost):
    o0, c4 = O[0].values, C[4].values
    hi5, lo5 = H.loc[:, 0:4].max(axis=1).values, L.loc[:, 0:4].min(axis=1).values
    d = np.sign(c4 - o0)
    entry = O[5].values
    stop = np.where(d > 0, lo5, hi5)
    Ls, Hs = L.loc[:, 5:].values, H.loc[:, 5:].values
    hit = np.where(d[:, None] > 0, Ls <= stop[:, None], Hs >= stop[:, None])
    first = np.where(hit.any(axis=1), hit.argmax(axis=1), -1)
    exit_px = C[389].values.copy()
    Os = O.loc[:, 5:].values
    rows = np.arange(len(d))
    has = first >= 0
    gap_px = Os[rows[has], first[has]]
    exit_px[has] = np.where(d[has] > 0, np.minimum(stop[has], gap_px), np.maximum(stop[has], gap_px))
    r1 = d * (exit_px / entry - 1) - 2 * cost * (d != 0)
    risk = np.abs(entry - stop) / entry
    lev = np.minimum(4.0, 0.01 / np.where(risk > 0, risk, np.nan))
    return to_series(r1, C.index), to_series(np.nan_to_num(lev) * r1, C.index)


def noise_area(O, H, L, C, V, cost, daily_ret):
    o0 = O[0]
    prev_c = C[389].shift(1)
    move = (C.div(o0, axis=0) - 1).abs()
    sig = move.rolling(14, min_periods=14).mean().shift(1)  # média dos últimos 14 dias, por minuto do dia
    ub = (np.maximum(o0, prev_c).values[:, None]) * (1 + sig.values)
    lb = (np.minimum(o0, prev_c).values[:, None]) * (1 - sig.values)
    vwap = (C * V).cumsum(axis=1) / V.cumsum(axis=1).replace(0, np.nan)
    Cv, Vw = C.values, vwap.values
    checks = list(range(30, 390, 30))  # 10:00, 10:30, ..., 15:30
    pos = np.zeros(len(C))
    ret = np.zeros(len(C))
    last = Cv[:, checks[0]].copy()
    for i, k in enumerate(checks):
        px = Cv[:, k]
        if i > 0:
            ret += pos * (px / last - 1)
        new = pos.copy()
        new[px > ub[:, k]] = 1
        new[px < lb[:, k]] = -1
        exit_long = (pos == 1) & (px < np.maximum(ub[:, k], Vw[:, k]))
        exit_short = (pos == -1) & (px > np.minimum(lb[:, k], Vw[:, k]))
        new[exit_long & ~(px > ub[:, k])] = 0
        new[exit_short & ~(px < lb[:, k])] = 0
        ret -= np.abs(new - pos) * cost
        pos, last = new, px
    ret += pos * (Cv[:, 389] / last - 1) - np.abs(pos) * cost
    r1 = pd.Series(np.nan_to_num(ret), index=C.index)
    vol14 = daily_ret.rolling(14).std().shift(1)
    lev = (0.02 / vol14).clip(upper=4.0).fillna(0)
    return r1, r1 * lev


def intraday_mom(C, cost):
    prev_c = C[389].shift(1)
    first = C[29] / prev_c - 1
    last = C[389] / C[359] - 1
    return (np.sign(first) * last - 2 * cost).fillna(0)


def gap_fade(O, H, L, C, cost, thr=0.003):
    prev_c = C[389].shift(1)
    gap = O[0] / prev_c - 1
    d = -np.sign(gap).where(gap.abs() > thr, 0)
    # sai no fechamento das 10:30 (k=60) ou quando o gap fecha
    target = prev_c
    Hs, Ls = H.loc[:, 0:60], L.loc[:, 0:60]
    filled = np.where(d > 0, (Hs.ge(target, axis=0)).any(axis=1), (Ls.le(target, axis=0)).any(axis=1))
    exit_px = np.where(filled, target, C[60])
    return (d * (exit_px / O[0] - 1) - 2 * cost * (d != 0)).fillna(0)


def popular_5m(reg, cost):
    b = reg[["open", "high", "low", "close", "volume"]].resample("5min", label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}).dropna()
    day = b.index.normalize()
    last_bar = pd.Series(b.index, index=b.index).groupby(day).transform("max") == b.index
    tp = (b.high + b.low + b.close) / 3
    vw = (tp * b.volume).groupby(day).cumsum() / b.volume.groupby(day).cumsum()
    r = rsi(b.close, 14)
    sigs = {
        "MME 9/21 (5m)": np.sign(ema(b.close, 9) - ema(b.close, 21)),
        "RSI 14 30/70 (5m)": state(r < 30, r > 50, r > 70, r < 50),
        "Preço vs VWAP (5m)": np.sign(b.close - vw),
    }
    out = {}
    for name, pos in sigs.items():
        pos = pd.Series(pos, index=b.index).fillna(0)
        pos[last_bar.values] = 0.0          # day trade: zera no último candle
        first_bar = ~day.duplicated()
        for mode, p in [("líquido", pos), ("fade líquido", -pos)]:
            rr = backtest(b, p, cost)
            rr[first_bar] = 0.0               # não carrega o gap da noite
            out[(name, mode)] = rr.groupby(day).sum()
    return out


def main():
    reg, O, H, L, C, V = load()
    daily_ret = C[389].pct_change()
    md = ["# Resultados — Day trade em ações (SPY, 1 minuto, 2008–2021)\n",
          f"{len(C)} pregões. IS 2008–2015, OOS 2016–2021. Retornos diários, anualização 252.\n"]
    rows = []
    for cost, lab in [(0.0001, "custo 1 pb/lado"), (0.000025, "custo 0,25 pb/lado")]:
        r1, rl = orb(O, H, L, C, cost)
        rows += split_stats(f"ORB 5 min · 1× · {lab}", r1, **KW)
        rows += split_stats(f"ORB 5 min · risco 1%/trade até 4× (artigo) · {lab}", rl, **KW)
        n1, nl = noise_area(O, H, L, C, V, cost, daily_ret)
        rows += split_stats(f"Zona de ruído · 1× · {lab}", n1, **KW)
        rows += split_stats(f"Zona de ruído · vol-alvo 2%/dia até 4× (artigo) · {lab}", nl, **KW)
        rows += split_stats(f"Momentum 1ª→última meia hora · {lab}", intraday_mom(C, cost), **KW)
        rows += split_stats(f"Fade de gap > 0,3% · {lab}", gap_fade(O, H, L, C, cost), **KW)
    on = (O[0] / C[389].shift(1) - 1).fillna(0)
    intra = (C[389] / O[0] - 1).fillna(0)
    rows += split_stats("Só overnight (fechamento→abertura)", on, **KW)
    rows += split_stats("Só intradiário (abertura→fechamento)", intra, **KW)
    rows += split_stats("Buy & hold SPY", daily_ret.fillna(0), **KW)
    for (name, mode), r in popular_5m(reg, 0.0001).items():
        rows += split_stats(f"{name} · {mode} · 1 pb", r, **KW)
    md += [table(rows), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
