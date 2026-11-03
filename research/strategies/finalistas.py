"""As 3 estratégias finalistas, em detalhe (curvas, ano a ano, sensibilidade a custos).

1. Tendência em BTC/ETH (média de 23 regras, long/caixa) — técnica
2. Carry de funding (delta-neutro) e a combinação "tendência + carry no caixa" — long/short
3. Momentum + Valor em ações brasileiras (NEFIN) — fundamentalista/quantitativa

Saídas: research/results/finalistas.md e gráficos PNG na mesma pasta.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import DATA, btc_long, fmt_table, nefin_daily, perf, run_signal  # noqa: E402
from signals import ready_date, trend_ensemble, vol_target  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
PPY = 365
C_SPOT, C_PERP = 0.0015, 0.0008
md = ["# Finalistas — análise detalhada\n", "Gerado por `research/strategies/finalistas.py`.\n"]


def spot(sym):
    return pd.read_csv(DATA / f"binance/spot_1d/{sym}USDT.csv", parse_dates=["date"]).set_index("date")["close"].astype(float)


def perp(sym):
    return pd.read_csv(DATA / f"binance/perp_1d/{sym}USDT.csv", parse_dates=["date"]).set_index("date")["close"].astype(float)


def funding(sym):
    df = pd.read_csv(DATA / f"binance/funding/{sym}USDT.csv")
    t = pd.to_datetime(df["time"], utc=True, format="mixed").dt.tz_convert(None)
    s = pd.Series(df["rate"].astype(float).values, index=t)
    return s.groupby(s.index.floor("D")).sum()


def table(items, ppy, periods, rf=None):
    rows = []
    for name, r in items:
        for label, a, b in periods:
            sub = r[a:b]
            p = perf(sub, ppy, rf=rf)
            rows.append({"estratégia": name, "período": label, "CAGR": p["CAGR"], "vol": p["vol"],
                         "sharpe": p["sharpe"], "maxDD": p["maxDD"], "calmar": p["calmar"]})
    return fmt_table(rows)


def yearly(items):
    df = pd.DataFrame({n: (1 + r).groupby(r.index.year).prod() - 1 for n, r in items})
    rows = [{"ano": int(y), **{c: f"{v*100:.0f}%" for c, v in row.items()}} for y, row in df.iterrows()]
    return fmt_table(rows)


def chart(series: dict[str, pd.Series], title: str, fname: str, ylab="Patrimônio (log, início = 1)"):
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    for name, r in series.items():
        eq = (1 + r.fillna(0)).cumprod()
        ax.plot(eq.index, eq.values, label=name, lw=1.4)
        ax2.plot(eq.index, (eq / eq.cummax() - 1).values * 100, lw=1)
    ax.set_yscale("log"); ax.set_title(title); ax.set_ylabel(ylab); ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3); ax2.set_ylabel("Drawdown %"); ax2.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(RES / fname, dpi=130); plt.close(fig)


# =============================================================== 1. tendência
md.append("## 1. Tendência em BTC/ETH — média de 23 regras (long/caixa)\n")
md.append("Posição diária = fração das 23 regras de tendência que estão compradas (0 a 100%). "
          "Nenhum parâmetro foi escolhido olhando o resultado: todas as regras da grade entram com o mesmo peso.\n")
bl = btc_long()
t0 = ready_date(bl)
rbl = bl.pct_change().fillna(0)[t0:]
ens_bl = trend_ensemble(bl)[t0:]
items = [("BTC buy & hold", rbl), ("BTC tendência", run_signal(rbl, ens_bl, C_SPOT)),
         ("BTC tendência + vol-alvo 50%", run_signal(rbl, vol_target(ens_bl, rbl, 0.5), C_SPOT)),
         ("BTC tendência (custo 2×)", run_signal(rbl, ens_bl, 2 * C_SPOT))]
md += ["### 1a. BTC desde 2012 (Bitstamp)\n",
       table(items, PPY, [(f"{t0:%Y-%m}–2026", t0, "2026"), (f"{t0:%Y-%m}–2019", t0, "2019"), ("2020–2026", "2020", "2026")]), "\n"]
chart({k: v for k, v in items[:2]}, f"BTC: buy & hold vs tendência (média de 23 regras), {t0:%Y}–2026", "f1_tendencia_btc.png")

btc, eth = spot("BTC"), spot("ETH")
btc_sig = bl.reindex(btc.index).ffill()      # sinal do BTC com histórico desde 2011
e0 = ready_date(eth)                          # ETH só depois do aquecimento das 23 regras
rb, re_ = btc.pct_change().fillna(0)["2018":], eth.pct_change().fillna(0)[e0:]
ens_btc, ens_eth = trend_ensemble(btc_sig), trend_ensemble(eth)
tb = run_signal(rb, ens_btc, C_SPOT)
te = run_signal(re_, ens_eth, C_SPOT)
idx = rb.index.intersection(re_.index)
items2 = [("BTC buy & hold", rb), ("BTC tendência", tb), ("ETH buy & hold", re_), ("ETH tendência", te),
          ("50/50 BTC+ETH buy & hold", 0.5 * rb.reindex(idx) + 0.5 * re_.reindex(idx)),
          ("50/50 BTC+ETH tendência", 0.5 * tb.reindex(idx) + 0.5 * te.reindex(idx))]
md += [f"### 1b. Binance (BTC desde 2018; ETH e 50/50 desde {e0:%Y-%m-%d}, após o aquecimento das regras)\n",
       table(items2, PPY, [("início–2026", "2018", "2026"), ("início–2022", "2018", "2022"), ("2023–2026", "2023", "2026")]), "\n",
       "### 1c. Ano a ano (Binance)\n", yearly(items2), "\n"]

# =============================================================== 2. carry
md.append("## 2. Carry de funding e \"tendência + carry no caixa\"\n")
md.append("Carry puro: compra spot + vende perpétuo na mesma quantidade (exposição zero ao preço) e recebe o funding. "
          "Tendência + carry: mantém 100% do capital em spot e vende perpétuo na fração `1 − sinal de tendência`; "
          "assim, quando a tendência manda sair, a posição fica neutra e passa a receber funding em vez de ficar parada. "
          "Exige conta com margem unificada (spot como garantia). Inclui custos e a oscilação diária spot×perpétuo.\n")
out_items, combos = [], {}
for sym, sig, r_s in [("BTC", ens_btc, rb), ("ETH", ens_eth, re_)]:
    pp, fd = perp(sym), funding(sym)
    d0 = pp.index[0]
    r_s2 = r_s[d0:]
    r_p = pp.pct_change().reindex(r_s2.index).fillna(0)
    f = fd.reindex(r_s2.index).fillna(0)
    carry = (f + r_s2 - r_p)
    carry.iloc[0] -= C_SPOT + C_PERP
    w = sig.reindex(r_s2.index).fillna(0)
    h = (1 - w).shift(1).fillna(1.0)  # fração vendida no perpétuo (decidida na véspera)
    combo = r_s2 - h * r_p + h * f - h.diff().abs().fillna(0) * C_PERP
    combo.iloc[0] -= C_SPOT
    trend_only = run_signal(r_s, sig, C_SPOT)[d0:]
    combos[sym] = (combo, trend_only, r_s2, carry)
    out_items += [(f"{sym} buy & hold", r_s2), (f"{sym} tendência (caixa 0%)", trend_only),
                  (f"{sym} tendência + carry no caixa", combo), (f"{sym} carry puro (1× capital)", carry),
                  (f"{sym} carry puro (1,5× capital)", carry / 1.5)]
md += [table(out_items, PPY, [("2020–2026", "2020", "2026"), ("2020–2022", "2020", "2022"), ("2023–2026", "2023", "2026")]), "\n",
       "### 2b. Ano a ano — BTC\n",
       yearly([("buy & hold", combos["BTC"][2]), ("tendência", combos["BTC"][1]),
               ("tendência + carry", combos["BTC"][0]), ("carry puro", combos["BTC"][3])]), "\n"]
chart({"BTC buy & hold": combos["BTC"][2], "BTC tendência (caixa 0%)": combos["BTC"][1],
       "BTC tendência + carry no caixa": combos["BTC"][0], "BTC carry puro": combos["BTC"][3]},
      "BTC 2020–2026: tendência com caixa remunerado por funding", "f2_tendencia_carry_btc.png")

# =============================================================== 3. ações BR
md.append("## 3. Momentum + Valor em ações brasileiras (NEFIN-USP, 2001–2026)\n")
nf = nefin_daily()
cdi = nf["RF"]
pm = pd.read_csv(DATA / "nefin/portfolio_by_momentum.csv", parse_dates=["date"]).set_index("date")["high"]
pv = pd.read_csv(DATA / "nefin/portfolio_by_book_to_market.csv", parse_dates=["date"]).set_index("date")["high"]
fee = pd.read_csv(DATA / "nefin/average_loan_fee.csv", parse_dates=["date"]).set_index("date")["average_loan_fee"]
fee = fee.reindex(nf.index).ffill().fillna(fee.mean()) / 100 * 1.5  # 1,5× a taxa média de aluguel (conservador)
lo = 0.5 * pm + 0.5 * pv - 0.01 / 252                     # long-only, ~1% a.a. de custo de giro
ls_raw = 0.5 * nf["WML"] + 0.5 * nf["HML"]
ls = cdi + ls_raw - 0.02 / 252 - fee / 252                # colateral em Tesouro Selic (CDI) + long-short − giro − aluguel
items3 = [("CDI", cdi), ("Mercado (índice NEFIN)", nf["MKT"]), ("Só momentum alto (long-only)", pm - 0.01 / 252),
          ("Momentum + Valor long-only", lo), ("CDI + Momentum/Valor long-short", ls)]
md += ["Long-only = 50% no terço de maior momentum + 50% no terço de maior valor patrimonial/preço, custo de giro de ~1% a.a. "
       "Long-short = 50% WML + 50% HML com colateral em Tesouro Selic (rende CDI), menos ~2% a.a. de giro e 1,5× a taxa média "
       "de aluguel de ações medida pelo NEFIN. Sharpe medido contra o CDI.\n",
       table(items3, 252, [("2001–2026", "2001", "2026"), ("2001–2013", "2001", "2013"), ("2014–2026", "2014", "2026")], rf=cdi), "\n",
       "### 3b. Ano a ano\n", yearly(items3), "\n"]
chart({k: v for k, v in items3}, "Brasil 2001–2026: momentum + valor vs mercado e CDI", "f3_acoes_br.png")

(RES / "finalistas.md").write_text("\n".join(md))
print("\n".join(md))
