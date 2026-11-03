"""Bloco M: ser a contraparte do day trader — reversão à média com ORDENS LIMITADAS
(maker) nas bandas de Bollinger de 5 min, com simulação de execução realista.

Regras
- No fechamento de cada barra de 5 min calcula média e desvio de 20 barras.
- Sem posição: deixa ordem limitada de COMPRA na banda inferior e de VENDA na superior,
  válidas durante a barra seguinte. Só considera executada se o preço ATRAVESSAR o nível
  em `through` (fila/seleção adversa): low ≤ nível × (1 − through).
- Com posição: deixa ordem limitada de saída na média móvel (atualizada a cada barra),
  executada se o preço atravessar. Stop de tempo: se não sair em `max_bars` barras,
  zera a mercado (paga taxa taker + slippage). Stop de preço opcional em k desvios.
- Entrada e saída nunca na mesma barra (conservador).

Saída: research/results/intraday_maker.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import COST, SYMS, load_1m, resample, split_stats, table  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "intraday_maker.md"


def simulate(b: pd.DataFrame, maker_fee: float, taker_cost: float, through: float = 0.0001,
             n: int = 20, k: float = 2.0, max_bars: int = 12, stop_k: float | None = 4.0):
    o, h, l, c = (b[x].values for x in ("open", "high", "low", "close"))
    m = pd.Series(c).rolling(n).mean().values
    sd = pd.Series(c).rolling(n).std().values
    pnl = np.zeros(len(c))         # retorno por barra (mark-to-market no fechamento)
    pos, entry_px, age, last_mark = 0, 0.0, 0, 0.0
    trades = 0
    for t in range(n, len(c) - 1):
        lo_lvl, hi_lvl, mid, s = m[t] - k * sd[t], m[t] + k * sd[t], m[t], sd[t]
        j = t + 1  # ordens válidas durante a barra seguinte
        if pos == 0:
            if l[j] <= lo_lvl * (1 - through):
                px = min(lo_lvl, o[j])  # se abrir abaixo do nível, executa na abertura (melhor preço)
                pos, entry_px, age, trades = 1, px, 0, trades + 1
                pnl[j] += c[j] / px - 1 - maker_fee
                last_mark = c[j]
            elif h[j] >= hi_lvl * (1 + through):
                px = max(hi_lvl, o[j])
                pos, entry_px, age, trades = -1, px, 0, trades + 1
                pnl[j] += -(c[j] / px - 1) - maker_fee
                last_mark = c[j]
            continue
        age += 1
        exit_px, fee = None, 0.0
        if pos == 1:
            if stop_k and l[j] <= entry_px - stop_k * s:
                exit_px, fee = min(o[j], entry_px - stop_k * s), taker_cost
            elif h[j] >= mid * (1 + through):
                exit_px, fee = max(mid, o[j]), maker_fee
        else:
            if stop_k and h[j] >= entry_px + stop_k * s:
                exit_px, fee = max(o[j], entry_px + stop_k * s), taker_cost
            elif l[j] <= mid * (1 - through):
                exit_px, fee = min(mid, o[j]), maker_fee
        if exit_px is None and age >= max_bars:
            exit_px, fee = c[j], taker_cost
        if exit_px is not None:
            pnl[j] += pos * (exit_px / last_mark - 1) - fee
            pos = 0
        else:
            pnl[j] += pos * (c[j] / last_mark - 1)
            last_mark = c[j]
    return pd.Series(pnl, index=b.index), trades


def main():
    scen = [("maker 0,02% (VIP0) · atravessar 1bp", 0.0002, 0.0001),
            ("maker 0,02% · atravessar 3bp (fila pior)", 0.0002, 0.0003),
            ("maker 0% (VIP alto/programa MM) · 1bp", 0.0, 0.0001),
            ("maker 0,02% · sem exigir atravessar (otimista)", 0.0002, 0.0)]
    port, per = {}, []
    for sym in SYMS:
        m1 = load_1m(sym)
        b = resample(m1, "5min")
        del m1
        for name, mf, thr in scen:
            r, tr = simulate(b, mf, COST[sym], thr)
            d = (1 + r).groupby(r.index.floor("D")).prod() - 1
            port.setdefault(name, []).append(d.rename(sym))
            per.append({"cenário": name, "ativo": sym[:-4], "trades/dia": round(tr / max(len(d), 1), 1)})
        print(sym, "ok", flush=True)
    rows = []
    for name, series in port.items():
        d = pd.concat(series, axis=1).mean(axis=1)
        rows += split_stats(name, d.rename(None))
    md = ["# Resultados — Contraparte do day trader: reversão com ordens limitadas (maker)\n",
          "Bollinger(20, 2) em 5 min, carteira igual BTC/ETH/SOL/DOGE/XRP (perpétuos). Entrada e alvo com ordem limitada; "
          "stop de 4 desvios e stop de tempo de 1h a mercado (taxa taker + slippage). Funding não incluído (posições < 1h na média).\n",
          table(rows), "\n", "### Operações por dia\n", table(per), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
