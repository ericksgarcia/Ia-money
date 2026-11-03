"""Núcleo do estudo intradiário: dados de 1 minuto, reamostragem, motor de
backtest com custos/funding e métricas mensais (foco na meta de 5% ao mês).

Convenções
- Posição decidida no fechamento da barra t vale para o retorno da barra t+1.
- Custo cobrado por unidade de giro |Δposição| (taxa agressora + slippage).
- Perpétuos: funding cobrado nos horários 00/08/16 UTC sobre a posição aberta
  (comprado paga taxa positiva; vendido recebe).
- "Fade" = mesma estratégia com sinal invertido, mesmos custos.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import fmt_table, perf  # noqa: E402,F401

DATA = Path(os.environ.get("DATA_DIR", "/home/user/rawdata"))
INTRA = DATA / "intraday"
SYMS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "XRPUSDT"]
# custo por lado: taxa taker VIP0 0,05% + slippage (0,01% BTC/ETH, 0,02% demais)
COST = {"BTCUSDT": 0.0006, "ETHUSDT": 0.0006, "SOLUSDT": 0.0007, "DOGEUSDT": 0.0007, "XRPUSDT": 0.0007}
IS_END, OOS_START = "2023-12-31", "2024-01-01"


# ----------------------------------------------------------------- dados
def load_1m(sym: str) -> pd.DataFrame:
    df = pd.read_parquet(INTRA / f"{sym}_1m.parquet")
    df.index = pd.to_datetime(df.pop("open_time"), unit="ms")
    return df[~df.index.duplicated()].sort_index()


def resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum",
           "quote_volume": "sum", "taker_buy_quote": "sum"}
    out = df.resample(rule, label="left", closed="left").agg({k: v for k, v in agg.items() if k in df})
    return out.dropna(subset=["close"])


def load_funding(sym: str) -> pd.Series:
    f = pd.read_csv(DATA / f"binance/funding/{sym}.csv")
    t = pd.to_datetime(f["time"], utc=True, format="mixed").dt.tz_convert(None).dt.floor("min")
    return pd.Series(f["rate"].astype(float).values, index=t).groupby(level=0).sum()


def load_metrics(sym: str) -> pd.DataFrame:
    m = pd.read_parquet(INTRA / f"{sym}_metrics.parquet").set_index("ts").sort_index()
    return m[~m.index.duplicated()]


# ----------------------------------------------------------------- motor
def backtest(bars: pd.DataFrame, pos: pd.Series, cost: float, funding: pd.Series | None = None) -> pd.Series:
    """Retorno por barra de uma série de posições (−1..1)."""
    pos = pos.reindex(bars.index).ffill().fillna(0.0).astype(float)
    ret = bars["close"].pct_change().fillna(0.0)
    held = pos.shift(1).fillna(0.0)
    r = held * ret - pos.diff().abs().fillna(pos.abs()) * cost
    if funding is not None:
        # funding pago no instante t sobre a posição em aberto durante a barra que contém t
        f = funding[(funding.index >= bars.index[0]) & (funding.index <= bars.index[-1])]
        loc = bars.index.searchsorted(f.index, side="right") - 1
        fr = np.zeros(len(bars))
        np.add.at(fr, loc, f.values)
        r = r - held * fr
    return r


def daily(r: pd.Series) -> pd.Series:
    return (1 + r).groupby(r.index.floor("D")).prod() - 1


def monthly(d: pd.Series) -> pd.Series:
    return (1 + d).groupby(d.index.to_period("M")).prod() - 1


def stats(d: pd.Series, label: str = "", trades_per_day: float | None = None, ppy: int = 365) -> dict:
    """Métricas focadas na pergunta '5% ao mês?'."""
    d = d.dropna()
    if len(d) < 20:
        return {}
    p = perf(d, ppy)
    m = monthly(d)
    out = {"período": label, "CAGR": p["CAGR"], "sharpe": p["sharpe"], "maxDD": p["maxDD"],
           "média_mês": float(m.mean()), "mediana_mês": float(m.median()),
           "%meses≥5%": f"{(m >= 0.05).mean()*100:.0f}%", "pior_mês": float(m.min())}
    if trades_per_day is not None:
        out["trades/dia"] = round(trades_per_day, 1)
    return out


def split_stats(name: str, r: pd.Series, pos: pd.Series | None = None, extra: dict | None = None,
                ppy: int = 365, is_end: str = IS_END, oos_start: str = OOS_START, labels=("IS 2020–2023", "OOS 2024–2026")) -> list[dict]:
    d = daily(r)
    rows = []
    tpd = None
    if pos is not None:
        p = pos.reindex(r.index).ffill().fillna(0)
        tpd = float(p.diff().abs().gt(0).groupby(p.index.floor("D")).sum().mean())
    for label, sub in [("total", d), (labels[0], d[:is_end]), (labels[1], d[oos_start:])]:
        s = stats(sub, label, tpd, ppy)
        if s:
            rows.append({"estratégia": name, **(extra or {}), **s})
    return rows


PCT = {"CAGR", "maxDD", "média_mês", "mediana_mês", "pior_mês"}


def table(rows: list[dict]) -> str:
    def f(k, v):
        if isinstance(v, float):
            return "—" if np.isnan(v) else (f"{v*100:.1f}%" if k in PCT else f"{v:.2f}")
        return str(v)
    if not rows:
        return "(vazio)"
    cols = list(dict.fromkeys(k for r in rows for k in r))
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    return head + "\n".join("| " + " | ".join(f(c, r.get(c, "")) for c in cols) + " |" for r in rows)


# ----------------------------------------------------------------- indicadores
def ema(x: pd.Series, n: int) -> pd.Series:
    return x.ewm(span=n, adjust=False).mean()


def rsi(x: pd.Series, n: int = 14) -> pd.Series:
    d = x.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def atr(b: pd.DataFrame, n: int = 14) -> pd.Series:
    pc = b["close"].shift(1)
    tr = pd.concat([b["high"] - b["low"], (b["high"] - pc).abs(), (b["low"] - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def supertrend(b: pd.DataFrame, n: int = 10, mult: float = 3.0) -> pd.Series:
    hl2 = ((b["high"] + b["low"]) / 2).values
    a = atr(b, n).values
    c = b["close"].values
    ub, lb = hl2 + mult * a, hl2 - mult * a
    fub, flb = ub.copy(), lb.copy()
    d = np.ones(len(c))
    for i in range(1, len(c)):
        fub[i] = ub[i] if (ub[i] < fub[i - 1] or c[i - 1] > fub[i - 1]) else fub[i - 1]
        flb[i] = lb[i] if (lb[i] > flb[i - 1] or c[i - 1] < flb[i - 1]) else flb[i - 1]
        if d[i - 1] == 1:
            d[i] = -1 if c[i] < flb[i] else 1
        else:
            d[i] = 1 if c[i] > fub[i] else -1
    return pd.Series(d, index=b.index)


def state(entry_long, exit_long, entry_short=None, exit_short=None) -> pd.Series:
    """Máquina de estados vetorizada: entradas/saídas → posição."""
    lng = pd.Series(np.nan, index=entry_long.index)
    lng[exit_long.fillna(False)] = 0.0
    lng[entry_long.fillna(False)] = 1.0
    pos = lng.ffill().fillna(0.0)
    if entry_short is not None:
        sht = pd.Series(np.nan, index=entry_short.index)
        sht[exit_short.fillna(False)] = 0.0
        sht[entry_short.fillna(False)] = -1.0
        pos = pos + sht.ffill().fillna(0.0)
    return pos.clip(-1, 1)
