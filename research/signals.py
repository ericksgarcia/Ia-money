"""Sinais de tendência compartilhados pelo estudo e pelas finalistas.

Cada regra devolve NaN enquanto não há histórico suficiente para calculá-la,
para que o período de aquecimento não seja confundido com "ficar em caixa".
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from lib import sma


def trend_positions(px: pd.Series) -> dict[str, pd.Series]:
    """As 23 regras de tendência testadas (1 = comprado, 0 = caixa, NaN = sem histórico)."""
    out = {}
    for n in [10, 20, 30, 50, 100, 150, 200]:
        m = sma(px, n)
        out[f"preço>MM{n}"] = (px > m).astype(float).where(m.notna())
    for f_, s_ in [(5, 50), (10, 50), (20, 100), (50, 200), (10, 100), (20, 200)]:
        slow = sma(px, s_)
        out[f"MM{f_}>MM{s_}"] = (sma(px, f_) > slow).astype(float).where(slow.notna())
    for n in [20, 50, 100]:
        hi, lo = px.rolling(n).max(), px.rolling(n // 2).min()
        p = pd.Series(np.nan, index=px.index)
        p[px >= hi] = 1.0
        p[px <= lo] = 0.0
        out[f"Donchian {n}/{n//2}"] = p.ffill().fillna(0.0).where(hi.notna())
    for n in [7, 14, 30, 60, 90, 180, 365]:
        past = px.shift(n)
        out[f"TSMOM {n}d"] = (px / past > 1).astype(float).where(past.notna())
    return out


def ready_date(px: pd.Series) -> pd.Timestamp:
    """Primeira data em que todas as 23 regras têm histórico suficiente."""
    return pd.DataFrame(trend_positions(px)).notna().all(axis=1).idxmax()


def trend_ensemble(px: pd.Series) -> pd.Series:
    """Média simples das 23 regras, SEM escolher as melhores (evita overfitting).
    Resultado em [0, 1] = fração do capital comprada; NaN antes de `ready_date`."""
    pos = pd.DataFrame(trend_positions(px))
    return pos.mean(axis=1).where(pos.notna().all(axis=1))


def vol_target(pos: pd.Series, ret: pd.Series, target: float, window: int = 30, ppy: int = 365) -> pd.Series:
    """Reduz a posição quando a volatilidade realizada passa do alvo (nunca alavanca)."""
    vol = ret.rolling(window, min_periods=window).std() * np.sqrt(ppy)
    return pos * (target / vol).clip(upper=1.0)
