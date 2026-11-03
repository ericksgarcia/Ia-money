"""Bloco W: "ímãs de liquidação" reconstruídos a partir do open interest.

A cada 15 min, o aumento de open interest (OI) é tratado como posições novas abertas ao
preço atual — divididas entre compradas e vendidas pela proporção do fluxo agressor — com
alavancagens típicas {5×, 10×, 20×, 50×, 100×}. Cada posição gera um nível de liquidação
(comprado: P·(1 − 1/L + 0,5%); vendido: P·(1 + 1/L − 0,5%)). Quedas de OI reduzem todos os
níveis proporcionalmente; níveis atravessados pelo preço são removidos (liquidados).
Hipótese ("caça à liquidez"): o preço é atraído pelo lado com mais liquidações próximas (±5%).
Saída: research/results/mat_liquidez.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intraday"))
from core import COST, IS_END, OOS_START, SYMS, backtest, daily, load_1m, load_funding, load_metrics, split_stats, table  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "mat_liquidez.md"
LEV = np.array([5, 10, 20, 50, 100.0])
LW = np.array([0.15, 0.30, 0.30, 0.15, 0.10])
BIN = 0.002  # 0,2% em log-preço


def heat(sym):
    c = load_1m(sym).close.resample("15min").last().dropna()
    m = load_metrics(sym).resample("15min").agg({"oi": "last", "taker_ls_vol": "mean"})
    df = pd.concat([c.rename("p"), m], axis=1).dropna()
    lp = np.log(df.p.values)
    lo, hi = lp.min() - 1.0, lp.max() + 1.0
    nb = int((hi - lo) / BIN) + 1
    L = np.zeros(nb)   # liquidações de comprados (abaixo do preço)
    S = np.zeros(nb)   # liquidações de vendidos (acima do preço)
    oi = df.oi.values
    tk = df.taker_ls_vol.values
    up_mass, dn_mass = np.zeros(len(df)), np.zeros(len(df))
    prev_bin = int((lp[0] - lo) / BIN)
    decay = 0.5 ** (1 / (14 * 96))  # meia-vida de 14 dias
    for t in range(1, len(df)):
        b = int((lp[t] - lo) / BIN)
        # níveis atravessados são liquidados
        if b < prev_bin:
            L[b:prev_bin + 1] = 0.0
        elif b > prev_bin:
            S[prev_bin:b + 1] = 0.0
        d_oi = oi[t] - oi[t - 1]
        if d_oi > 0:
            notional = d_oi * df.p.values[t]
            long_share = tk[t] / (1 + tk[t]) if np.isfinite(tk[t]) else 0.5
            lb = ((lp[t] + np.log(1 - 1 / LEV + 0.005) - lo) / BIN).astype(int)
            sb = ((lp[t] + np.log(1 + 1 / LEV - 0.005) - lo) / BIN).astype(int)
            np.add.at(L, lb, notional * long_share * LW)
            np.add.at(S, sb, notional * (1 - long_share) * LW)
        elif d_oi < 0 and oi[t - 1] > 0:
            f = max(0.0, 1 + d_oi / oi[t - 1])
            L *= f
            S *= f
        L *= decay
        S *= decay
        w = int(0.05 / BIN)
        up_mass[t] = S[b + 1:b + 1 + w].sum()
        dn_mass[t] = L[max(b - w, 0):b].sum()
        prev_bin = b
    out = pd.DataFrame({"p": df.p, "up": up_mass, "dn": dn_mass}, index=df.index)
    out["imb"] = (out.up - out.dn) / (out.up + out.dn).replace(0, np.nan)
    out["oi_usd"] = df.oi * df.p
    return out


def main():
    md = ["# Resultados — Ímãs de liquidação (reconstruídos do open interest)\n",
          "`imb` > 0 = mais liquidações de vendidos acima do preço (combustível para alta) do que de comprados abaixo.\n"]
    ev, port = [], {}
    for sym in SYMS:
        hm = heat(sym).resample("1h").last().dropna()
        fwd = {k: hm.p.shift(-k) / hm.p - 1 for k in (4, 24)}
        q = hm.imb[:IS_END].quantile([0.2, 0.8]).values
        for per, sl in [("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))]:
            x = hm[sl]
            for k, f in fwd.items():
                top = f[sl][x.imb > q[1]].dropna()
                bot = f[sl][x.imb < q[0]].dropna()
                spread = top.mean() - bot.mean()
                se = np.sqrt(top.var() / max(len(top) / k, 1) + bot.var() / max(len(bot) / k, 1))
                ev.append({"ativo": sym[:-4], "período": per, "horizonte": f"{k}h",
                           "ret. quando ímã ACIMA": f"{top.mean()*100:+.2f}%", "ret. quando ímã ABAIXO": f"{bot.mean()*100:+.2f}%",
                           "diferença": f"{spread*100:+.2f}%", "t (ajustado)": round(float(spread / se), 2)})
        bars = pd.DataFrame({"close": hm.p})
        pos = pd.Series(np.where(hm.imb > q[1], 1.0, np.where(hm.imb < q[0], -1.0, 0.0)), index=hm.index)
        pos = pos.rolling(24, min_periods=1).mean()
        for mode, p in [("a favor do ímã", pos), ("contra o ímã", -pos)]:
            port.setdefault(mode, []).append(daily(backtest(bars, p, COST[sym], load_funding(sym))).rename(sym))
        print(sym, flush=True)
    rows = []
    for mode, ser in port.items():
        rows += split_stats(f"Ímã de liquidação · {mode}", pd.concat(ser, axis=1).mean(axis=1).rename(None))
    md += ["## W1. Retorno futuro conforme o lado do ímã (quintis definidos no IS)\n", table(ev), "\n",
           "## W2. Estratégia (carteira dos 5 ativos, 24 tranches, custos + funding)\n", table(rows), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
