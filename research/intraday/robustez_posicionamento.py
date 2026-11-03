"""Robustez dos sinais de posicionamento: atraso extra (1h/2h, elimina qualquer
dúvida sobre o horário de publicação das métricas), limiar do z-score e prazo
de manutenção. Saída: research/results/intraday_posicionamento_robustez.md
"""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import COST, SYMS, backtest, daily, load_funding, stats, table  # noqa: E402
from posicionamento import hold, panel, z  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "intraday_posicionamento_robustez.md"


def main():
    data = {}
    for sym in SYMS:
        _, h = panel(sym)
        data[sym] = (h, load_funding(sym))
        print(sym, flush=True)
    rows = []
    grid = list(product(["varejo", "divergência"], [0, 1, 2], [1.5, 2.0, 2.5], [8, 24, 48]))
    for sig, lag, thr, H in grid:
        series = []
        for sym, (h, fund) in data.items():
            za, zt = z(h.acc_ls).shift(lag), z(h.top_pos_ls).shift(lag)
            if sig == "varejo":
                el, es = za < -thr, za > thr
            else:
                el, es = (zt > thr / 2) & (za < -thr / 2), (zt < -thr / 2) & (za > thr / 2)
            pos = hold(el.fillna(False), H) - hold(es.fillna(False), H)
            series.append(daily(backtest(h, pos, COST[sym], fund)).rename(sym))
        d = pd.concat(series, axis=1).mean(axis=1)
        s_is, s_oos = stats(d[:"2023"]), stats(d["2024":])
        rows.append({"sinal": sig, "atraso_h": lag, "limiar_z": thr, "segura_h": H,
                     "IS média/mês": f"{s_is['média_mês']*100:+.1f}%", "IS sharpe": round(s_is["sharpe"], 2),
                     "OOS média/mês": f"{s_oos['média_mês']*100:+.1f}%", "OOS sharpe": round(s_oos["sharpe"], 2),
                     "OOS maxDD": f"{s_oos['maxDD']*100:.0f}%", "OOS %meses≥5%": s_oos["%meses≥5%"]})
    df = pd.DataFrame(rows)
    md = ["# Robustez — sinais de posicionamento\n",
          "`varejo` = contra a razão long/short das contas; `divergência` = top traders comprados enquanto o varejo vende "
          "(limiar dividido por 2 em cada perna). Atraso = horas extras entre a métrica e a decisão.\n",
          "## Resumo: % das variantes com Sharpe OOS > 0\n",
          table([{"sinal": s, "atraso_h": a, "variantes": len(g), "%OOS>0": f"{(g['OOS sharpe'] > 0).mean()*100:.0f}%",
                  "Sharpe OOS mediano": round(g["OOS sharpe"].median(), 2)} for (s, a), g in df.groupby(["sinal", "atraso_h"])]),
          "\n## Grade completa\n", table(rows), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md[:4]))


if __name__ == "__main__":
    main()
