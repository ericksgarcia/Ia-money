"""Bloco L: "ir contra o varejo" com dados reais de posicionamento (Binance, 5 min)
e microestrutura intradiária com dados de 1 minuto.

L1. O que o varejo faz: correlação entre a razão long/short das contas e o preço.
L2. Sinais de posicionamento (contrários ou a favor), estudo de eventos + versão operável:
    - razão long/short de TODAS as contas (proxy do varejo) em extremo
    - razão long/short das POSIÇÕES dos top traders (proxy de "dinheiro grande")
    - divergência top traders × varejo
    - fluxo agressor (taker buy/sell) em extremo
    - cascata de liquidação (preço cai forte + open interest despenca) e short squeeze
    - funding em extremo
L3. Sazonalidade intradiária (hora do dia, horário do funding, fim de semana) e
    reação a movimentos extremos de 1 minuto.

Saída: research/results/intraday_posicionamento.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import (COST, IS_END, OOS_START, SYMS, backtest, daily, load_1m, load_funding,  # noqa: E402
                  load_metrics, split_stats, table)

OUT = Path(__file__).resolve().parents[1] / "results" / "intraday_posicionamento.md"
H = 24  # horizonte de manutenção (horas) na versão operável


def z(x: pd.Series, n: int = 168) -> pd.Series:
    return (x - x.rolling(n, min_periods=n // 2).mean()) / x.rolling(n, min_periods=n // 2).std()


def hold(ev: pd.Series, n: int) -> pd.Series:
    return ev.astype(float).rolling(n, min_periods=1).max()


def panel(sym: str):
    m1 = load_1m(sym)
    h = m1.resample("1h", label="left", closed="left").agg({"open": "first", "high": "max", "low": "min", "close": "last",
                                                             "quote_volume": "sum", "taker_buy_quote": "sum"}).dropna()
    met = load_metrics(sym).resample("1h", label="right", closed="right").last()  # valor conhecido no fim da hora
    met.index = met.index - pd.Timedelta("1h")  # alinhado à barra que termina nesse instante
    h = h.join(met[["oi_value", "top_pos_ls", "acc_ls", "top_acc_ls"]], how="left")
    h["taker_ratio"] = h["taker_buy_quote"] / (h["quote_volume"] - h["taker_buy_quote"])
    h = h[h.index >= met.dropna().index.min()]
    return m1, h


def event_rows(sym, h, name, el, es, fund, c):
    """Estudo de eventos (retorno futuro médio) + estratégia operável (segura H horas)."""
    fwd = {k: h.close.shift(-k) / h.close - 1 for k in (1, 4, 24)}
    rows = []
    for label, a, b in [("IS", None, IS_END), ("OOS", OOS_START, None)]:
        sl = slice(a, b)
        sig = (el.astype(int) - es.astype(int))[sl]
        n = int((sig != 0).sum())
        if n < 10:
            continue
        r = {"sinal": name, "ativo": sym[:-4], "período": label, "eventos": n}
        for k, f in fwd.items():
            x = (f[sl] * sig).where(sig != 0).dropna()
            r[f"ret_{k}h"] = f"{x.mean()*100:+.2f}%"
            if k == 24:
                r["t_24h"] = round(float(x.mean() / (x.std() / np.sqrt(max(len(x) / 24, 1)))), 2)  # t ajustado p/ sobreposição
        rows.append(r)
    pos = hold(el, H) - hold(es, H)
    return rows, pos


def main():
    md = ["# Resultados — Posicionamento da multidão e microestrutura\n",
          "Dados: métricas de 5 min da Binance (open interest, razão long/short das contas e dos top traders, fluxo agressor) "
          "e candles de 1 min dos perpétuos. Sinais calculados no fechamento de cada hora; versão operável segura 24h. "
          f"IS até {IS_END[:4]}, OOS {OOS_START[:4]}–2026. Retornos futuros já com o sinal aplicado (positivo = o sinal acertou).\n"]
    beh, ev_rows, port, hours = [], [], {}, []
    for sym in SYMS:
        m1, h = panel(sym)
        fund = load_funding(sym)
        c = COST[sym]
        print(sym, len(h), h.index[0], flush=True)
        ret24 = h.close.pct_change(24)
        d_acc = h.acc_ls.pct_change(24)
        beh.append({"ativo": sym[:-4],
                    "% contas compradas (média)": f"{(h.acc_ls / (1 + h.acc_ls)).mean()*100:.0f}%",
                    "corr(Δ long/short 24h, retorno 24h)": round(float(d_acc.corr(ret24)), 2),
                    "corr(Δ long/short 24h, retorno PRÓXIMAS 24h)": round(float(d_acc.corr(h.close.shift(-24) / h.close - 1)), 2),
                    "corr(top traders Δ24h, retorno próximas 24h)": round(float(h.top_pos_ls.pct_change(24).corr(h.close.shift(-24) / h.close - 1)), 2)})

        za, zt = z(h.acc_ls), z(h.top_pos_ls)
        zf = z(np.log(h.taker_ratio.replace(0, np.nan)))
        r1 = h.close.pct_change()
        doi = h.oi_value.pct_change()
        zr, zoi = z(r1, 720), z(doi, 720)
        fh = fund.reindex(h.index, method="ffill")
        fq_hi = fh.rolling(24 * 90, min_periods=24 * 30).quantile(0.95)
        fq_lo = fh.rolling(24 * 90, min_periods=24 * 30).quantile(0.05)
        sigs = {
            "Contra o varejo: contas muito compradas → vende (e vice-versa)": (za < -2, za > 2),
            "A favor dos top traders: posições compradas → compra": (zt > 2, zt < -2),
            "Top traders compram enquanto varejo vende": ((zt > 1) & (za < -1), (zt < -1) & (za > 1)),
            "Contra o fluxo agressor extremo": (zf < -2.5, zf > 2.5),
            "Cascata de liquidação: queda forte + OI despenca → compra": ((zr < -3) & (zoi < -2), (zr > 3) & (zoi < -2)),
            "Contra o funding extremo": (fh < fq_lo, fh > fq_hi),
        }
        for name, (el, es) in sigs.items():
            el, es = el.fillna(False), es.fillna(False)
            rows, pos = event_rows(sym, h, name, el, es, fund, c)
            ev_rows += rows
            for mode, p, cc in [("líquido", pos, c), ("fade líquido", -pos, c)]:
                port.setdefault((name, mode), []).append(daily(backtest(h, p, cc, fund)).rename(sym))

        # L3: hora do dia (UTC) com 1 minuto → retorno médio por hora, IS vs OOS
        r = m1.close.pct_change()
        hr = r.groupby([r.index.year >= 2024, r.index.hour]).mean().unstack(0)
        hr.columns = ["IS", "OOS"]
        hr["ativo"] = sym[:-4]
        hours.append(hr)
        # reação a movimento extremo de 1 minuto
        zz = r / r.rolling(1440, min_periods=720).std()
        for k in (5, 15, 60):
            f = m1.close.shift(-k) / m1.close - 1
            for lab, msk in [("subida >5σ", zz > 5), ("queda <−5σ", zz < -5)]:
                for per, sl in [("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))]:
                    x = f[sl][msk[sl]].dropna()
                    if len(x) > 20:
                        ev_rows.append({"sinal": f"Após candle 1m {lab} (próx. {k} min)", "ativo": sym[:-4], "período": per,
                                        "eventos": len(x), "ret_k_min": f"{x.mean()*100:+.3f}%",
                                        "t_24h": round(float(x.mean() / (x.std() / np.sqrt(len(x)))), 2)})
        del m1

    md += ["## L1. O que o varejo faz\n",
           "A razão long/short das contas mede quantas contas estão compradas vs vendidas (cada conta pesa igual, então é dominada pelo varejo).\n",
           table(beh), "\n"]

    rows = []
    for (name, mode), series in port.items():
        d = pd.concat(series, axis=1).mean(axis=1)
        rows += split_stats(name, d.rename(None), extra={"modo": mode})
    md += ["## L2. Sinais de posicionamento — estratégia operável (carteira dos 5 ativos, segura 24h, custos + funding)\n",
           table(rows), "\n",
           "## L2b. Estudo de eventos por ativo (retorno futuro médio na direção do sinal)\n",
           table(ev_rows), "\n"]

    hrs = pd.concat(hours)
    prof = hrs.groupby(level=0)[["IS", "OOS"]].mean() * 1e4  # pontos-base por minuto × 1e4 → bp
    corr = prof["IS"].corr(prof["OOS"])
    best_is = prof["IS"].nlargest(4).index.tolist()
    md += ["## L3. Sazonalidade por hora (UTC), média dos 5 ativos — retorno médio por minuto em centésimos de bp\n",
           f"Correlação do perfil horário IS × OOS: **{corr:.2f}** (perto de 0 = padrão não se repete). "
           f"4 melhores horas no IS: {best_is}; retorno dessas horas no OOS: "
           f"{prof.loc[best_is, 'OOS'].mean():+.3f} vs média geral {prof['OOS'].mean():+.3f}.\n",
           table([{"hora_UTC": int(i), "IS": f"{v.IS:+.3f}", "OOS": f"{v.OOS:+.3f}"} for i, v in prof.iterrows()]), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md[:4]))


if __name__ == "__main__":
    main()
