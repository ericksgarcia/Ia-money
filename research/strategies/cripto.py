"""Estudo de estratégias em CRIPTO (Binance 2017–2026, todos os pares USDT,
inclusive deslistados; BTC desde 2011 via Bitstamp).

Blocos
 E. Referências (buy & hold BTC, ETH, carteira igual top-10)
 F. Tendência de série temporal (MM, cruzamentos, Donchian, TSMOM) — grade de
    parâmetros com seleção in-sample e avaliação out-of-sample; long/caixa e long/short
 G. Reversão à média (RSI(2), Bollinger, quedas consecutivas)
 H. Momentum e reversão cross-section (ranking entre moedas), long-only e long-short
 I. Carry de funding (cash-and-carry: compra spot + vende perpétuo)
 J. Sazonalidade (dia da semana) e padrões de candle (estudo de eventos)

Saída: research/results/cripto.md
"""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import DATA, btc_long, fmt_table, perf, rsi, run_signal, sma  # noqa: E402
from signals import ready_date, trend_positions  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "cripto.md"
PPY = 365
C_SPOT = 0.0015   # 0,10% taxa + 0,05% slippage por lado
C_PERP = 0.0008   # 0,05% taxa + 0,03% slippage por lado
IS_END, OOS_START = "2022-12-31", "2023-01-01"
EXCLUDE = {"WBTC", "WBETH", "BETH", "PAXG", "XAUT", "STETH", "USTC", "EURI", "AEUR"}
md: list[str] = ["# Resultados — Cripto\n",
                 "Gerado por `research/strategies/cripto.py`. Dados diários (UTC). Caixa = USDT a 0% (conservador). "
                 f"Custos: spot {C_SPOT*100:.2f}%/lado, perpétuo {C_PERP*100:.2f}%/lado + funding real. "
                 f"In-sample até {IS_END[:4]}, out-of-sample {OOS_START[:4]}–2026.\n"]
TRIALS = {"n": 0}
TRIALS_EST = 250  # estimativa fixa do nº total de variantes testadas (conservadora) para o DSR


# ----------------------------------------------------------------- dados
def load_panel():
    C, Q, O, H, L = {}, {}, {}, {}, {}
    for f in sorted((DATA / "binance/spot_1d").glob("*.csv")):
        sym = f.stem[:-4]
        if sym in EXCLUDE:
            continue
        df = pd.read_csv(f, parse_dates=["date"]).set_index("date")
        if len(df) < 60:
            continue
        C[sym], Q[sym], O[sym], H[sym], L[sym] = df.close, df.quote_volume, df.open, df.high, df.low
    idx = pd.date_range("2017-08-17", max(s.index.max() for s in C.values()), freq="D")
    mk = lambda d: pd.DataFrame({k: v[~v.index.duplicated()] for k, v in d.items()}).reindex(idx)  # noqa: E731
    C, Q, O, H, L = mk(C), mk(Q), mk(O), mk(H), mk(L)
    R = C.pct_change(fill_method=None)
    # quebra de série (relistagem com mesmo ticker, ex.: LUNA): retorno após buraco > 7 dias = NaN
    for col in C.columns:
        s = C[col]
        valid = s.dropna()
        if valid.empty:
            continue
        gaps = valid.index.to_series().diff().dt.days
        for d in gaps[gaps > 7].index:
            R.loc[d, col] = np.nan
    R = R.clip(-0.95, 3.0)  # proteção contra erros grosseiros
    return C, R, Q, O, H, L


def load_funding(cols, idx) -> pd.DataFrame:
    F = {}
    for f in sorted((DATA / "binance/funding").glob("*.csv")):
        sym = f.stem[:-4]
        if sym not in cols:
            continue
        df = pd.read_csv(f)
        if df.empty:
            continue
        df["time"] = pd.to_datetime(df["time"], utc=True, format="mixed").dt.tz_convert(None)
        s = df.set_index("time")["rate"].astype(float)
        F[sym] = s.groupby(s.index.floor("D")).sum()
    return pd.DataFrame(F).reindex(idx)


C, R, Q, O, H, L = load_panel()
F = load_funding(set(C.columns), C.index)
print(f"painel: {C.shape[1]} moedas, {C.index[0].date()}→{C.index[-1].date()}; funding: {F.shape[1]} perpétuos", flush=True)
md.append(f"Universo: **{C.shape[1]} pares USDT** (inclui deslistados), {C.index[0].date()} → {C.index[-1].date()}; "
          f"funding de **{F.shape[1]} perpétuos**.\n")

# universo ponto-a-ponto: top-N por volume médio de 30 dias, com ≥ 120 dias de histórico
age = C.notna().cumsum()
vol30 = Q.rolling(30, min_periods=20).mean().where(age >= 120)
vrank = vol30.rank(axis=1, ascending=False)


def periods(r: pd.Series, start="2018-01-01"):
    r = r[start:]
    return [("2018–2026", r), ("IS 2018–2022", r[:IS_END]), ("OOS 2023–2026", r[OOS_START:])]


def row(name, r, held=None, extra=None, start="2018-01-01"):
    out = []
    for label, sub in periods(r, start):
        p = perf(sub, PPY, trials=TRIALS_EST)
        d = {"estratégia": name, "período": label, "CAGR": p["CAGR"], "vol": p["vol"], "sharpe": p["sharpe"],
             "maxDD": p["maxDD"], "calmar": p["calmar"]}
        if held is not None:
            d["exposicao"] = float(held.reindex(sub.index).abs().mean())
        if extra:
            d.update(extra)
        d["DSR"] = p["DSR"]
        out.append(d)
    return out


# =============================================================== E. referências
btc, eth = C["BTC"], C["ETH"]
rb, re_ = R["BTC"].fillna(0), R["ETH"].fillna(0)
top10 = (vrank <= 10)
w_ew = top10.div(top10.sum(axis=1), axis=0).fillna(0)
w_ew_m = w_ew.loc[w_ew.index.is_month_end].reindex(w_ew.index).ffill().fillna(0)  # rebal. mensal
r_ew = (w_ew_m.shift(1) * R.fillna(0)).sum(axis=1) - w_ew_m.diff().abs().sum(axis=1).shift(1).fillna(0) * C_SPOT
rows = row("Buy & hold BTC", rb) + row("Buy & hold ETH", re_) + row("Top-10 por volume, pesos iguais (mensal)", r_ew)
md += ["## E. Referências (buy & hold)\n", fmt_table(rows), "\n"]
BH_OOS = {"BTC": perf(rb[OOS_START:], PPY)["sharpe"], "ETH": perf(re_[OOS_START:], PPY)["sharpe"]}


# =============================================================== F. tendência
def trend_grid(px: pd.Series, ret: pd.Series, fund: pd.Series | None, name: str, start: str, is_end: str, oos_start: str):
    start = str(max(pd.Timestamp(start), ready_date(px)).date())  # só compara depois do aquecimento de todas as regras
    res = []
    for k, pos in trend_positions(px).items():
        for mode in ["long/caixa", "long/short"]:
            p = pos if mode == "long/caixa" else pos * 2 - 1
            r = run_signal(ret, p, C_SPOT if mode == "long/caixa" else C_PERP)
            if mode == "long/short" and fund is not None:  # vendido em perpétuo recebe funding
                r = r + (-p.shift(1).clip(upper=0)) * fund.reindex(r.index).fillna(0)
            r = r[start:]
            res.append({"ativo": name, "regra": k, "modo": mode,
                        "sh_IS": perf(r[:is_end], PPY)["sharpe"], "sh_OOS": perf(r[oos_start:], PPY)["sharpe"],
                        "CAGR_OOS": perf(r[oos_start:], PPY)["CAGR"], "maxDD_OOS": perf(r[oos_start:], PPY)["maxDD"],
                        "r": r})
    TRIALS["n"] += len(res)
    return res


grids = []
grids += trend_grid(btc_long(), btc_long().pct_change().fillna(0), None, "BTC 2012–2026 (Bitstamp)", "2012-01-01", "2019-12-31", "2020-01-01")
btc_sig = btc_long().reindex(C.index).ffill()  # sinal do BTC com histórico desde 2011 (preço é o mesmo em qualquer corretora)
grids += trend_grid(btc_sig, rb, F.get("BTC"), "BTC (Binance)", "2018-01-01", IS_END, OOS_START)
grids += trend_grid(eth, re_, F.get("ETH"), f"ETH (Binance, desde {ready_date(eth).date()})", "2018-01-01", IS_END, OOS_START)
G = pd.DataFrame([{k: v for k, v in g.items() if k != "r"} for g in grids])

summary = []
for (ativo, modo), sub in G.groupby(["ativo", "modo"], sort=False):
    best = sub.sort_values("sh_IS", ascending=False).iloc[0]
    summary.append({"ativo": ativo, "modo": modo, "regras": len(sub),
                    "mediana_sh_IS": sub.sh_IS.median(), "mediana_sh_OOS": sub.sh_OOS.median(),
                    "%_OOS>0": f"{(sub.sh_OOS > 0).mean()*100:.0f}%",
                    "melhor_IS": best.regra, "sh_IS": best.sh_IS, "→ sh_OOS": best.sh_OOS,
                    "CAGR_OOS": best.CAGR_OOS, "maxDD_OOS": best.maxDD_OOS})
md += ["## F. Tendência — grade de parâmetros (escolhe a melhor regra no IS, mede no OOS)\n",
       "BTC longo: IS 2012–2019, OOS 2020–2026. Binance: IS 2018–2022, OOS 2023–2026. "
       f"Sharpe OOS do buy & hold: BTC {BH_OOS['BTC']:.2f}, ETH {BH_OOS['ETH']:.2f}.\n",
       fmt_table(summary), "\n"]
top_rules = G[G.modo == "long/caixa"].groupby("regra")[["sh_IS", "sh_OOS"]].mean().sort_values("sh_OOS", ascending=False)
md += ["### F2. Robustez: Sharpe médio de cada regra (long/caixa) nos 3 testes — top 10 e piores 5\n",
       fmt_table([{"regra": k, "sh_IS": v.sh_IS, "sh_OOS": v.sh_OOS} for k, v in top_rules.head(10).iterrows()]), "\n",
       fmt_table([{"regra": k, "sh_IS": v.sh_IS, "sh_OOS": v.sh_OOS} for k, v in top_rules.tail(5).iterrows()]), "\n"]

# tendência aplicada a uma cesta (top-20 por volume): cada moeda 1/20 se acima da MM, senão caixa
rows = []
for n in [20, 50, 100]:
    elig = (vrank <= 20)
    sig = (C > sma(C, n)) & elig
    w = sig.astype(float) / 20.0
    turnover = w.diff().abs().sum(axis=1)
    r = (w.shift(1) * R.fillna(0)).sum(axis=1) - turnover.shift(1).fillna(0) * C_SPOT
    TRIALS["n"] += 1
    rows += row(f"Cesta top-20, cada moeda > MM{n} (long/caixa)", r, held=w.sum(axis=1))
md += ["### F3. Tendência em cesta diversificada (top-20 por volume)\n", fmt_table(rows), "\n"]

# =============================================================== G. reversão à média
rows = []
for sym, px, ret in [("BTC", btc, rb), ("ETH", eth, re_)]:
    r2 = rsi(px, 2)
    p1 = pd.Series(np.nan, index=px.index); p1[r2 < 10] = 1.0; p1[px > sma(px, 5)] = 0.0
    p2 = pd.Series(np.nan, index=px.index); p2[(r2 < 10) & (px > sma(px, 200))] = 1.0; p2[px > sma(px, 5)] = 0.0
    m, sd = sma(px, 20), px.rolling(20).std()
    p3 = pd.Series(np.nan, index=px.index); p3[px < m - 2 * sd] = 1.0; p3[px > m] = 0.0
    down3 = (ret < 0) & (ret.shift(1) < 0) & (ret.shift(2) < 0)
    p4 = pd.Series(np.nan, index=px.index); p4[down3] = 1.0; p4[ret > 0] = 0.0
    p5 = pd.Series(np.nan, index=px.index); p5[r2 > 90] = -1.0; p5[px < sma(px, 5)] = 0.0  # short em sobrecompra
    for name, p, c in [("RSI(2)<10, sai > MM5", p1, C_SPOT), ("RSI(2)<10 acima MM200", p2, C_SPOT),
                       ("Bollinger(20,2) inferior → média", p3, C_SPOT), ("Compra após 3 quedas", p4, C_SPOT),
                       ("Short RSI(2)>90 (perp)", p5, C_PERP)]:
        p = p.ffill().fillna(0.0)
        r = run_signal(ret, p, c)
        TRIALS["n"] += 1
        rows += row(f"{sym}: {name}", r, held=p.shift(1))
md += ["## G. Reversão à média (BTC/ETH, diário)\n", fmt_table(rows), "\n"]


# =============================================================== H. cross-section
def xs_portfolio(lookback: int, n_univ: int, q: float, mode: str, reb: int = 7,
                 btc_filter: int | None = None, reverse: bool = False, k_long: int | None = None):
    score = C / C.shift(lookback) - 1
    if reverse:
        score = -score
    elig = (vrank <= n_univ) & score.notna()
    shortable = F.notna().rolling(3, min_periods=1).max().reindex(columns=C.columns).fillna(0).astype(bool)
    reb_days = C.index[::reb]
    W = pd.DataFrame(0.0, index=reb_days, columns=C.columns)
    for d in reb_days:
        s = score.loc[d][elig.loc[d]]
        if len(s) < 10:
            continue
        nq = k_long or max(1, int(len(s) * q))
        longs = s.nlargest(nq).index
        W.loc[d, longs] = 1.0 / nq
        if mode == "long/short":
            s_sh = s[shortable.loc[d, s.index]]
            shorts = s_sh.nsmallest(nq).index
            if len(shorts):
                W.loc[d, longs] = 0.5 / nq
                W.loc[d, shorts] = -0.5 / len(shorts)
        if btc_filter and not (btc.loc[d] > sma(btc, btc_filter).loc[d]):
            W.loc[d] = 0.0
    W = W.reindex(C.index).ffill().fillna(0.0)
    held = W.shift(1).fillna(0.0)
    turnover = W.diff().abs().sum(axis=1).shift(1).fillna(0)
    long_cost = turnover * np.where(mode == "long/short", (C_SPOT + C_PERP) / 2, C_SPOT)
    r = (held * R.fillna(0)).sum(axis=1) - long_cost
    r = r + (-held.clip(upper=0) * F.reindex(columns=C.columns).fillna(0)).sum(axis=1)  # vendido recebe funding
    return r, held


rows_x = []
grid = list(product([7, 14, 30, 60, 90], [20, 50], ["long/short", "long-only"]))
for lb, nu, mode in grid:
    r, held = xs_portfolio(lb, nu, 0.2, mode)
    rows_x.append({"sinal": "momentum", "lookback": lb, "universo": nu, "modo": mode,
                   "sh_IS": perf(r["2018":IS_END], PPY)["sharpe"], "sh_OOS": perf(r[OOS_START:], PPY)["sharpe"],
                   "CAGR_OOS": perf(r[OOS_START:], PPY)["CAGR"], "maxDD_OOS": perf(r[OOS_START:], PPY)["maxDD"]})
for lb, nu in product([1, 3, 7], [20, 50]):
    r, _ = xs_portfolio(lb, nu, 0.2, "long/short", reb=1 if lb == 1 else 3, reverse=True)
    rows_x.append({"sinal": "reversão", "lookback": lb, "universo": nu, "modo": "long/short",
                   "sh_IS": perf(r["2018":IS_END], PPY)["sharpe"], "sh_OOS": perf(r[OOS_START:], PPY)["sharpe"],
                   "CAGR_OOS": perf(r[OOS_START:], PPY)["CAGR"], "maxDD_OOS": perf(r[OOS_START:], PPY)["maxDD"]})
TRIALS["n"] += len(rows_x)
md += ["## H. Cross-section (ranking entre moedas, quintis, rebalanceamento semanal)\n",
       "Vendido só em moedas com perpétuo listado na data; vendido recebe/paga funding real.\n",
       fmt_table(rows_x), "\n"]

rows = []
for lb, flt in [(30, None), (30, 50), (60, 50), (90, 100)]:
    r, held = xs_portfolio(lb, 50, 0.2, "long-only", btc_filter=flt, k_long=5)
    TRIALS["n"] += 1
    rows += row(f"Top-5 momentum {lb}d" + (f" + filtro BTC>MM{flt}" if flt else ""), r, held=held.sum(axis=1))
md += ["### H2. Momentum long-only concentrado (top-5 de 50) com/sem filtro de tendência do BTC\n", fmt_table(rows), "\n"]

# =============================================================== I. carry de funding
PERP = {s_: pd.read_csv(DATA / f"binance/perp_1d/{s_}USDT.csv", parse_dates=["date"]).set_index("date")["close"].reindex(C.index)
        for s_ in ["BTC", "ETH"]}
md += ["## I. Carry de funding (compra spot + vende perpétuo, delta-neutro)\n"]
fund_rows = []
for sym in ["BTC", "ETH"]:
    f = F[sym].dropna()
    by_year = f.groupby(f.index.year).agg(["sum", lambda s: (s < 0).mean()])
    for y, v in by_year.iterrows():
        fund_rows.append({"ativo": sym, "ano": int(y), "funding_anual": f"{v.iloc[0]*100:.1f}%",
                          "%dias_negativos": f"{v.iloc[1]*100:.0f}%"})
md += ["### I1. Funding anual acumulado (o que o vendido do perpétuo recebe)\n", fmt_table(fund_rows), "\n"]

rows = []
CAP = 1.5  # capital por unidade de notional: 1 no spot + 0,5 de margem no perpétuo
for name, syms, rule in [("BTC sempre", ["BTC"], "always"), ("ETH sempre", ["ETH"], "always"),
                         ("BTC+ETH, só se funding 7d > 0", ["BTC", "ETH"], "pos7"),
                         ("Top-5 funding 7d (entre top-30 vol.)", None, "top5")]:
    if rule == "top5":
        f7 = F.rolling(7, min_periods=7).mean().where(vrank.reindex(columns=F.columns) <= 30)
        reb_days = F.index[::7]
        W = pd.DataFrame(0.0, index=reb_days, columns=F.columns)
        for d in reb_days:
            s = f7.loc[d].dropna()
            s = s[s > 0].nlargest(5)
            if len(s):
                W.loc[d, s.index] = 1.0 / 5
        W = W.reindex(F.index).ffill().fillna(0)
    else:
        W = pd.DataFrame(0.0, index=F.index, columns=F.columns)
        for s_ in syms:
            if rule == "always":
                W[s_] = (F[s_].notna()).astype(float) / len(syms)
            else:
                W[s_] = (F[s_].rolling(7).mean() > 0).astype(float) / len(syms)
    held = W.shift(1).fillna(0)
    turnover = W.diff().abs().sum(axis=1).shift(1).fillna(0)
    # funding + descolamento spot×perpétuo (base) quando há candles do perpétuo
    basis = pd.DataFrame(0.0, index=F.index, columns=F.columns)
    for s_, pr in PERP.items():
        basis[s_] = (R[s_] - pr.pct_change(fill_method=None)).reindex(F.index).fillna(0)
    gross = (held * (F.fillna(0) + basis)).sum(axis=1)
    r = (gross - turnover * (C_SPOT + C_PERP)) / CAP
    r = r[r.index >= F[["BTC"]].dropna().index[0]]
    TRIALS["n"] += 1
    rows += row(f"Carry {name}", r, held=held.sum(axis=1), start="2019-09-10")
md += ["### I2. Retorno sobre o capital (capital = 1,5× notional; custos nas duas pernas; BTC/ETH incluem a oscilação diária spot×perpétuo; Top-5 só funding)\n",
       fmt_table(rows), "\n",
       "Risco não capturado no backtest: falência/bloqueio da corretora (ex.: FTX 2022), liquidação do vendido "
       "em alta brusca se a margem for curta, descolamento temporário entre spot e perpétuo.\n"]

# =============================================================== J. sazonalidade e candles
dow = rb["2018":].groupby(rb["2018":].index.dayofweek).agg(["mean", "std", "count"])
dow["t"] = dow["mean"] / (dow["std"] / np.sqrt(dow["count"]))
nomes = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
md += ["## J. Sazonalidade e padrões gráficos\n", "### J1. BTC — retorno médio por dia da semana (2018–2026)\n",
       fmt_table([{"dia": nomes[i], "media_diaria": f"{v['mean']*100:.3f}%", "t": v["t"]} for i, v in dow.iterrows()]), "\n"]

body = (C - O).abs()
rng = (H - L).replace(0, np.nan)
prev_bear = (C.shift(1) < O.shift(1))
patterns = {
    "Engolfo de alta": prev_bear & (C > O) & (O <= C.shift(1)) & (C >= O.shift(1)),
    "Martelo": ((np.minimum(O, C) - L) > 2 * body) & ((H - np.maximum(O, C)) < body) & (C.pct_change(5, fill_method=None) < 0),
    "Doji após queda": (body / rng < 0.1) & (C.pct_change(5, fill_method=None) < -0.05),
    "Três soldados": (C > O) & (C.shift(1) > O.shift(1)) & (C.shift(2) > O.shift(2)) & (C > C.shift(1)) & (C.shift(1) > C.shift(2)),
    "Rompimento máx. 20d": C >= C.rolling(20).max(),
}
fwd5 = C.shift(-5) / C - 1
univ = vrank <= 50
base = fwd5.where(univ)
rows = []
for name, mask in patterns.items():
    mk = mask.fillna(False) & univ
    for label, a, b in [("IS 2018–2022", "2018", IS_END), ("OOS 2023–2026", OOS_START, "2026")]:
        ev = fwd5.where(mk)[a:b].stack().dropna()
        bs = base[a:b].stack().dropna()
        excess = ev.mean() - bs.mean()
        t = excess / (ev.std() / np.sqrt(len(ev))) if len(ev) > 30 else np.nan
        rows.append({"padrão": name, "período": label, "eventos": len(ev),
                     "ret_5d_médio": f"{ev.mean()*100:.2f}%", "excesso_vs_média": f"{excess*100:.2f}%",
                     "t": t, "excesso_líq_custos": f"{(excess - 2*C_SPOT)*100:.2f}%"})
    TRIALS["n"] += 1
md += ["### J2. Padrões de candle — retorno 5 dias após o sinal vs média do universo (top-50)\n", fmt_table(rows), "\n"]

md.insert(1, f"Total aproximado de variantes testadas: **{TRIALS['n']}** (usado no Sharpe deflacionado).\n")
OUT.write_text("\n".join(md))
print("\n".join(md))
