"""Bloco O: setups brasileiros de day trade no mini-índice (WIN, 5 min, jun–out/2023).

Amostra curta (≈ 4 meses, dados exportados do ProfitPro e publicados no GitHub em
Bielhpp/MarketPrediction_WinfutBr-CandlestickChart) — serve só como ilustração.
Retornos sobre o valor nocional do contrato; custo 0,005%/lado (1 tick + emolumentos).
Saída: research/results/intraday_win.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import INTRA, backtest, ema, stats, table  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "intraday_win.md"
COST = 0.00005


def main():
    w = pd.read_excel(INTRA / "WIN_5m.xlsx")
    b = w.rename(columns={"Data": "t", "Abertura": "open", "Máxima": "high", "Mínima": "low", "Fechamento": "close",
                          "VWAP D": "vwap"}).set_index("t").sort_index()[["open", "high", "low", "close", "vwap"]]
    day = b.index.normalize()
    first = ~day.duplicated()
    last = pd.Series(b.index, index=b.index).groupby(day).transform("max") == b.index
    e9 = ema(b.close, 9)
    # 9.1: MME9 vira para cima → compra; vira para baixo → vende (zera no fim do dia)
    s91 = np.sign(e9 - e9.shift(1))
    # PFR de compra: mínima abaixo das 2 anteriores e fechamento acima do fechamento anterior → compra por 6 barras (30 min)
    pfr_c = (b.low < b.low.shift(1)) & (b.low < b.low.shift(2)) & (b.close > b.close.shift(1))
    pfr_v = (b.high > b.high.shift(1)) & (b.high > b.high.shift(2)) & (b.close < b.close.shift(1))
    spfr = pfr_c.astype(float).rolling(6, min_periods=1).max() - pfr_v.astype(float).rolling(6, min_periods=1).max()
    # ORB: rompimento do 1º candle de 5 min do dia, segura até o fim do dia
    fh = b.high.where(first).ffill()
    fl = b.low.where(first).ffill()
    up = (b.close > fh) & ~first
    dn = (b.close < fl) & ~first
    ev = pd.Series(np.where(up, 1.0, np.where(dn, -1.0, np.nan)), index=b.index)
    sorb = ev.groupby(day).transform(lambda s: s.where(s.notna().cumsum() >= 1).bfill().iloc[0] if s.notna().any() else 0.0)
    started = ev.notna().groupby(day).cumsum() > 0
    sorb = sorb.where(started, 0.0)
    svwap = np.sign(b.close - b.vwap)
    rows = []
    for name, pos in [("Setup 9.1 (MME9)", s91), ("PFR (preço de fechamento de reversão)", spfr),
                      ("ORB do 1º candle", sorb), ("Preço vs VWAP", svwap)]:
        pos = pd.Series(pos, index=b.index).fillna(0.0)
        pos[last.values] = 0.0
        for mode, p, c in [("bruto", pos, 0.0), ("líquido", pos, COST), ("fade líquido", -pos, COST)]:
            r = backtest(b, p, c)
            r[first] = 0.0
            d = r.groupby(day).sum()
            s = stats(d, "jun–out/2023", ppy=252)
            ntr = float((p.diff().abs() > 0).groupby(day).sum().mean())
            rows.append({"setup": name, "modo": mode, "trades/dia": round(ntr, 1), "dias": len(d),
                         "média_dia": f"{d.mean()*100:+.3f}%", "média_mês": s["média_mês"], "sharpe": s["sharpe"], "maxDD": s["maxDD"]})
    md = ["# Resultados — Setups brasileiros no mini-índice (WIN 5 min, jun–out/2023)\n",
          f"{day.nunique()} pregões, de {b.index[0]:%d/%m/%Y} a {b.index[-1]:%d/%m/%Y}. Retorno sobre o nocional (1 contrato ≈ "
          "R$ 24 mil); com a margem típica de day trade (centenas de reais) a alavancagem real é de dezenas de vezes. "
          "**Amostra curta demais para conclusões estatísticas.**\n", table(rows), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
