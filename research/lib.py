"""Núcleo do estudo: carregadores de dados, métricas e Sharpe deflacionado.

Convenções
- Retornos simples por período (fração, não %).
- Sinais são sempre defasados em 1 período antes de multiplicar o retorno
  (decide no fechamento de t, ganha o retorno de t+1): sem look-ahead.
- Custos: `cost` é a fração cobrada por unidade de giro (|Δposição|).
"""
from __future__ import annotations

import math
import os
import re
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

DATA = Path(os.environ.get("DATA_DIR", "/home/user/rawdata"))
N = NormalDist()

# ----------------------------------------------------------------- loaders


def _ff_first_block(path: Path, date_len: int) -> pd.DataFrame:
    """Lê o primeiro bloco de dados (mensal/diário) de um arquivo do Ken French."""
    lines = path.read_text(errors="ignore").splitlines()
    header, rows, started = None, [], False
    pat = re.compile(rf"^\s*(\d{{{date_len}}})\s*,")
    for i, ln in enumerate(lines):
        if pat.match(ln):
            if not started:
                started = True
                header = [h.strip() for h in lines[i - 1].split(",")]
            rows.append([c.strip() for c in ln.split(",")])
        elif started:
            break
    cols = ["date"] + header[1:]
    df = pd.DataFrame(rows, columns=cols[: len(rows[0])])
    fmt = "%Y%m" if date_len == 6 else "%Y%m%d"
    df["date"] = pd.to_datetime(df["date"], format=fmt)
    if date_len == 6:
        df["date"] = df["date"] + pd.offsets.MonthEnd(0)
    df = df.set_index("date").apply(pd.to_numeric, errors="coerce") / 100.0
    return df


def ff_monthly() -> pd.DataFrame:
    """Fatores EUA mensais (fração). Colunas: MKT (total), RF, MKT_RF, SMB, HML, RMW, CMA, UMD, STR, LTR, LOWBETA, LOWVOL."""
    ff3 = _ff_first_block(DATA / "ff/ff3_monthly.csv", 6)
    ff5 = _ff_first_block(DATA / "ff/ff5_monthly.csv", 6)
    mom = _ff_first_block(DATA / "ff/F-F_Momentum_Factor.csv", 6)
    st = _ff_first_block(DATA / "ff/F-F_ST_Reversal_Factor.csv", 6)
    lt = _ff_first_block(DATA / "ff/F-F_LT_Reversal_Factor.csv", 6)
    beta = _ff_first_block(DATA / "ff/Portfolios_Formed_on_BETA.csv", 6)
    var = _ff_first_block(DATA / "ff/Portfolios_Formed_on_VAR.csv", 6)
    df = pd.DataFrame(index=ff3.index)
    df["RF"] = ff3["RF"]
    df["MKT_RF"] = ff3["Mkt-RF"]
    df["MKT"] = df["MKT_RF"] + df["RF"]
    df["SMB"] = ff3["SMB"]
    df["HML"] = ff3["HML"]
    df = df.join(ff5[["RMW", "CMA"]], how="left")
    df["UMD"] = mom.iloc[:, 0]
    df["STR"] = st.iloc[:, 0]
    df["LTR"] = lt.iloc[:, 0]
    # quintis: colunas 0..4 = Lo 20 .. Hi 20 (valor ponderado)
    df["LOWBETA"] = beta.iloc[:, 0] - beta.iloc[:, 4]
    df["LOWVOL"] = var.iloc[:, 0] - var.iloc[:, 4]
    return df


def ff_daily() -> pd.DataFrame:
    d = _ff_first_block(DATA / "ff/ff3_daily.csv", 8)
    out = pd.DataFrame(index=d.index)
    out["RF"] = d["RF"]
    out["MKT"] = d["Mkt-RF"] + d["RF"]
    return out


def shiller() -> pd.DataFrame:
    df = pd.read_csv(DATA / "shiller/sp500_shiller.csv", parse_dates=["Date"]).set_index("Date")
    df.index = df.index + pd.offsets.MonthEnd(0)
    df = df.replace(0.0, np.nan)
    return df


def nefin_daily() -> pd.DataFrame:
    df = pd.read_csv(DATA / "nefin/nefin_factors.csv", parse_dates=["Date"]).set_index("Date")
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed") or c == ""], errors="ignore")
    df = df.rename(columns={"Rm_minus_Rf": "MKT_RF", "Risk_Free": "RF"})
    df["MKT"] = df["MKT_RF"] + df["RF"]
    return df


def btc_long() -> pd.Series:
    df = pd.read_csv(DATA / "btc/btc-usd-daily.csv", parse_dates=["date"]).set_index("date")
    return df["close"].astype(float)


# ----------------------------------------------------------------- métricas


def max_drawdown(r: pd.Series) -> float:
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def perf(r: pd.Series, ppy: float, rf: pd.Series | None = None, trials: int = 1) -> dict:
    r = r.dropna()
    if len(r) < 3:
        return {}
    ex = r - (rf.reindex(r.index).fillna(0.0) if rf is not None else 0.0)
    yrs = len(r) / ppy
    eq = float((1 + r).prod())
    cagr = eq ** (1 / yrs) - 1 if eq > 0 else -1.0
    vol = float(r.std() * math.sqrt(ppy))
    sd = float(ex.std())
    sr_p = float(ex.mean() / sd) if sd > 0 else 0.0
    mdd = max_drawdown(r)
    out = {
        "inicio": r.index[0].strftime("%Y-%m"),
        "fim": r.index[-1].strftime("%Y-%m"),
        "anos": round(yrs, 1),
        "CAGR": cagr,
        "vol": vol,
        "sharpe": sr_p * math.sqrt(ppy),
        "t": sr_p * math.sqrt(len(r)),
        "maxDD": mdd,
        "calmar": cagr / abs(mdd) if mdd < 0 else np.nan,
    }
    out["DSR"] = deflated_sharpe(ex, trials) if trials > 1 else psr(ex, 0.0)
    return out


def psr(ex: pd.Series, sr_bench_per_period: float) -> float:
    """Probabilistic Sharpe Ratio (Bailey & López de Prado)."""
    ex = ex.dropna()
    n = len(ex)
    sd = ex.std()
    if n < 10 or sd == 0:
        return np.nan
    sr = ex.mean() / sd
    skew = float(ex.skew())
    kurt = float(ex.kurt()) + 3.0
    denom = math.sqrt(max(1e-12, 1 - skew * sr + (kurt - 1) / 4 * sr**2))
    return N.cdf((sr - sr_bench_per_period) * math.sqrt(n - 1) / denom)


def deflated_sharpe(ex: pd.Series, trials: int, sr_var_per_period: float | None = None) -> float:
    """DSR: probabilidade de o Sharpe verdadeiro ser > 0 depois de descontar
    o melhor resultado esperado por sorte entre `trials` tentativas."""
    ex = ex.dropna()
    n = len(ex)
    if sr_var_per_period is None:
        sr_var_per_period = 1.0 / max(n - 1, 1)  # variância do SR sob H0
    g = 0.5772156649
    e = math.e
    sr0 = math.sqrt(sr_var_per_period) * ((1 - g) * N.inv_cdf(1 - 1 / trials) + g * N.inv_cdf(1 - 1 / (trials * e)))
    return psr(ex, sr0)


def fmt_table(rows: list[dict], cols: list[str] | None = None) -> str:
    """Tabela markdown com formatação de % e números."""
    if not rows:
        return "(vazio)"
    cols = cols or list(rows[0].keys())
    pct = {"CAGR", "vol", "maxDD", "media", "exposicao", "giro_anual"}

    def f(k, v):
        if isinstance(v, (float, np.floating)):
            if np.isnan(v):
                return "—"
            if k in pct:
                return f"{v * 100:.1f}%"
            if k == "DSR":
                return f"{v:.2f}"
            return f"{v:.2f}"
        return str(v)

    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    return head + "\n".join("| " + " | ".join(f(c, r.get(c, "")) for c in cols) + " |" for r in rows)


# ----------------------------------------------------------------- execução de sinais


def run_signal(ret: pd.Series, pos: pd.Series, cost: float, cash: pd.Series | None = None) -> pd.Series:
    """Aplica posição (decidida em t, válida em t+1) com custo por giro.
    pos: exposição (1 = comprado, 0 = caixa, -1 = vendido).
    Modelo de financiamento tipo futuro: r = cash + pos·(ret − cash) − custo.
    Com pos=1 rende o ativo; pos=0 rende o caixa; pos=−1 rende 2·cash − ret
    (vendido via futuro, colateral aplicado no caixa)."""
    pos = pos.reindex(ret.index).ffill().fillna(0.0)
    held = pos.shift(1).fillna(0.0)
    turnover = held.diff().abs().fillna(held.abs())
    c = cash.reindex(ret.index).fillna(0.0) if cash is not None else 0.0
    return c + held * (ret - c) - turnover * cost


def sma(x: pd.Series, n: int) -> pd.Series:
    return x.rolling(n, min_periods=n).mean()


def rsi(x: pd.Series, n: int) -> pd.Series:
    d = x.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))
