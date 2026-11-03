"""Bloco V: momentos que ninguém vê no gráfico (microestrutura, 1 minuto).

V1. BTC lidera as altcoins? Quando o BTC dá um salto de > 3σ no minuto e a altcoin ainda
    não acompanhou, o que a altcoin faz nos próximos 1–15 minutos?
V2. Fluxo forçado no pagamento do funding (00/08/16 UTC): com funding alto, quem está
    comprado tende a fechar antes de pagar → padrão de preço em torno do horário?
V3. Números redondos (Osler 2003): stops ficam logo depois de números redondos. Ao cruzar
    um número redondo, o movimento acelera? Controle: níveis "meio-redondos" deslocados.
Saída: research/results/mat_micro.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intraday"))
from core import COST, IS_END, OOS_START, SYMS, load_1m, load_funding, table  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "mat_micro.md"
ROUND = {"BTCUSDT": 1000.0, "ETHUSDT": 100.0, "SOLUSDT": 10.0, "XRPUSDT": 0.1, "DOGEUSDT": 0.01}


def ev_stats(x: pd.Series, label, per):
    x = x.dropna()
    if len(x) < 20:
        return None
    return {"evento": label, "período": per, "n": len(x), "média": f"{x.mean()*100:+.3f}%",
            "t": round(float(x.mean() / (x.std() / np.sqrt(len(x)))), 2), "% positivos": f"{(x > 0).mean()*100:.0f}%"}


def main():
    C = {s: load_1m(s)[["close"]] for s in SYMS}
    md = ["# Resultados — Microestrutura: momentos ocultos (1 minuto)\n",
          f"Custo de ida e volta para comparação: ≈ {2*COST['BTCUSDT']*100:.2f}% (BTC/ETH) e {2*COST['SOLUSDT']*100:.2f}% (demais).\n"]
    rows = []
    # V1 lead-lag
    btc = C["BTCUSDT"].close
    rb = btc.pct_change()
    zb = rb / rb.rolling(1440, min_periods=720).std()
    for s in ["ETHUSDT", "SOLUSDT", "DOGEUSDT", "XRPUSDT"]:
        alt = C[s].close.reindex(btc.index)
        ra = alt.pct_change()
        za = ra / ra.rolling(1440, min_periods=720).std()
        lag = (zb.abs() > 3) & (np.sign(za) != np.sign(zb)) | ((zb.abs() > 3) & (za.abs() < 1))
        for k in (1, 5, 15):
            fwd = (alt.shift(-k) / alt - 1) * np.sign(zb)
            for per, sl in [("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))]:
                r = ev_stats(fwd[sl][lag[sl]], f"BTC salta >3σ e {s[:-4]} fica para trás → {s[:-4]} nos próximos {k} min (na direção do BTC)", per)
                if r:
                    rows.append(r)
    md += ["## V1. BTC lidera as altcoins?\n", table(rows), "\n"]

    # V2 funding
    rows = []
    for s in SYMS:
        c = C[s].close
        f = load_funding(s)
        f = f[f.index >= c.index[0]]
        hi = f.abs() > f.abs().rolling(90, min_periods=30).quantile(0.8)
        for (a, b), lab in [((-60, -30), "−60→−30 min"), ((-30, 0), "−30 min→liquidação"), ((0, 30), "liquidação→+30 min"), ((30, 120), "+30→+120 min")]:
            ta, tb = f.index + pd.Timedelta(minutes=a), f.index + pd.Timedelta(minutes=b)
            pa = c.reindex(ta, method="ffill").values
            pb = c.reindex(tb, method="ffill").values
            ret = pd.Series((pb / pa - 1) * -np.sign(f.values), index=f.index)  # positivo = movimento contra quem paga
            for per, sl in [("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))]:
                r = ev_stats(ret[sl][hi[sl]], f"{s[:-4]} funding alto · {lab} (contra quem paga)", per)
                if r:
                    rows.append(r)
    md += ["## V2. Em torno do pagamento do funding (só quando o funding está no 20% mais alto)\n",
           "Sinal positivo = o preço anda contra o lado que paga o funding (ex.: cai quando os comprados pagam).\n", table(rows), "\n"]

    # V3 números redondos
    rows = []
    for s in SYMS:
        c = C[s].close
        step = ROUND[s]
        for lab, off in [("redondo", 0.0), ("controle (meio-redondo)", 0.5)]:
            lvl_prev = np.floor(c.shift(1) / step - off)
            lvl_now = np.floor(c / step - off)
            up = lvl_now > lvl_prev
            dn = lvl_now < lvl_prev
            # filtra cruzamentos "limpos" (um nível só) e preço não muito longe do nível
            for k in (5, 15, 60):
                fwd = c.shift(-k) / c - 1
                x = pd.concat([fwd[up], -fwd[dn]])
                for per, sl in [("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))]:
                    xx = x.sort_index()[sl]
                    r = ev_stats(xx, f"{s[:-4]} cruza nível {lab} (passo {step:g}) → próximos {k} min (continuação)", per)
                    if r:
                        rows.append(r)
    md += ["## V3. Números redondos vs níveis de controle\n", table(rows), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
