"""Bloco K: as estratégias de day trade mais populares (fóruns, YouTube,
TradingView, bots do GitHub) aplicadas a perpétuos de cripto com dados de
1 minuto — e o "fade" de cada uma (operar exatamente o contrário).

Ativos: BTC, ETH, SOL, DOGE, XRP (perpétuos USDT-M da Binance, 2020–2026).
Saída: research/results/intraday_daytrade_cripto.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import (COST, SYMS, backtest, daily, ema, load_1m, load_funding, resample,  # noqa: E402
                  rsi, split_stats, stats, state, supertrend, table)

OUT = Path(__file__).resolve().parents[1] / "results" / "intraday_daytrade_cripto.md"


# ----------------------------------------------------------------- estratégias (retornam barras, posição)
def s_ema_cross(m1, tf):
    b = resample(m1, tf)
    return b, np.sign(ema(b.close, 9) - ema(b.close, 21))


def s_macd(m1, tf):
    b = resample(m1, tf)
    macd = ema(b.close, 12) - ema(b.close, 26)
    return b, np.sign(macd - ema(macd, 9))


def s_rsi(m1, tf):
    b = resample(m1, tf)
    r = rsi(b.close, 14)
    return b, state(r < 30, r > 50, r > 70, r < 50)


def s_boll(m1, tf):
    b = resample(m1, tf)
    m, sd = b.close.rolling(20).mean(), b.close.rolling(20).std()
    return b, state(b.close < m - 2 * sd, b.close > m, b.close > m + 2 * sd, b.close < m)


def s_vwap(m1, tf):
    tp = (m1.high + m1.low + m1.close) / 3
    day = m1.index.floor("D")
    vw = (tp * m1.volume).groupby(day).cumsum() / m1.volume.groupby(day).cumsum()
    b = resample(m1, tf)
    v = vw.resample(tf, label="left", closed="left").last().reindex(b.index)
    return b, np.sign(b.close - v)


def s_supertrend(m1, tf):
    b = resample(m1, tf)
    return b, supertrend(b, 10, 3.0)


def s_91(m1, tf):
    b = resample(m1, tf)
    e = ema(b.close, 9)
    return b, np.sign(e - e.shift(1))  # 9.1 de compra (MME9 vira para cima) e de venda (vira para baixo)


def s_orb_ny(m1, _tf):
    """Opening Range Breakout na abertura de Nova York (15 min), saída no stop oposto ou às 16:00 ET."""
    ny = m1.index.tz_localize("UTC").tz_convert("America/New_York")
    mins = ny.hour * 60 + ny.minute
    nyday = ny.normalize().tz_localize(None)
    c, h, low = m1.close.values, m1.high.values, m1.low.values
    pos = np.zeros(len(m1))
    in_or = (mins >= 570) & (mins < 585)
    sess = (mins >= 585) & (mins < 960)
    df = pd.DataFrame({"d": nyday, "or": in_or, "s": sess})
    for _, idx in df.groupby("d").indices.items():
        o = idx[in_or[idx]]
        s = idx[sess[idx]]
        if len(o) < 10 or len(s) < 10:
            continue
        hi, lo = h[o].max(), low[o].min()
        d = 0
        for i in s:
            if d == 0:
                if c[i] > hi:
                    d = 1
                elif c[i] < lo:
                    d = -1
            elif (d == 1 and c[i] < lo) or (d == -1 and c[i] > hi):
                break  # stop no lado oposto da faixa
            pos[i] = d
        # zera no fim da sessão
    return m1, pd.Series(pos, index=m1.index)


def s_pdhl(m1, _tf):
    """Rompimento da máxima/mínima do dia anterior (UTC); segura até o fim do dia."""
    day = m1.index.floor("D")
    dh = m1.high.groupby(day).max().shift(1)
    dl = m1.low.groupby(day).min().shift(1)
    pdh, pdl = dh.reindex(day).values, dl.reindex(day).values
    up = pd.Series(m1.close.values > pdh, index=m1.index)
    dn = pd.Series(m1.close.values < pdl, index=m1.index)
    fu = up.groupby(day).cumsum() > 0
    fd = dn.groupby(day).cumsum() > 0
    first_up = up.groupby(day).transform(lambda s: s.values.argmax() if s.any() else 10**9)
    first_dn = dn.groupby(day).transform(lambda s: s.values.argmax() if s.any() else 10**9)
    pos = np.where(fu & (first_up < first_dn), 1.0, np.where(fd & (first_dn < first_up), -1.0, 0.0))
    pos = pd.Series(pos, index=m1.index)
    last = pd.Series(m1.index, index=m1.index).groupby(day).transform("max") == m1.index
    pos[last.values] = 0.0
    return m1, pos


def s_sweep(m1, tf):
    """ICT "liquidity sweep": fura a mínima (máxima) do dia anterior e fecha de volta dentro → compra (vende) por 4h."""
    b = resample(m1, tf)
    day = b.index.floor("D")
    pdl = b.low.groupby(day).min().shift(1).reindex(day).values
    pdh = b.high.groupby(day).max().shift(1).reindex(day).values
    el = pd.Series((b.low.values < pdl) & (b.close.values > pdl), index=b.index)
    es = pd.Series((b.high.values > pdh) & (b.close.values < pdh), index=b.index)
    n = int(pd.Timedelta("4h") / pd.Timedelta(tf))
    return b, el.astype(float).rolling(n, min_periods=1).max() - es.astype(float).rolling(n, min_periods=1).max()


def s_spike(m1, _tf):
    """Scalping de momentum: candle de 1 min > 4 desvios → segue por 15 min."""
    r = m1.close.pct_change()
    z = r / r.rolling(1440, min_periods=720).std()
    el, es = (z > 4).astype(float), (z < -4).astype(float)
    return m1, el.rolling(15, min_periods=1).max() - es.rolling(15, min_periods=1).max()


STRATS = [
    ("Cruzamento MME 9/21 (5m)", s_ema_cross, "5min"),
    ("Cruzamento MME 9/21 (15m)", s_ema_cross, "15min"),
    ("MACD 12/26/9 (15m)", s_macd, "15min"),
    ("RSI 14: compra <30, vende >70 (5m)", s_rsi, "5min"),
    ("RSI 14: compra <30, vende >70 (15m)", s_rsi, "15min"),
    ("Bollinger 20,2 reversão (5m)", s_boll, "5min"),
    ("Preço vs VWAP do dia (15m)", s_vwap, "15min"),
    ("Supertrend 10,3 (15m)", s_supertrend, "15min"),
    ("Supertrend 10,3 (1h)", s_supertrend, "1h"),
    ("Setup 9.1 Larry Williams (15m)", s_91, "15min"),
    ("Setup 9.1 Larry Williams (1h)", s_91, "1h"),
    ("ORB abertura de NY (1m)", s_orb_ny, None),
    ("Rompimento máx/mín do dia anterior (1m)", s_pdhl, None),
    ("ICT liquidity sweep (5m)", s_sweep, "5min"),
    ("Scalping de spike >4σ (1m)", s_spike, None),
]


def vol_breakout(m1, cost, k=0.5):
    """Rompimento de volatilidade de Larry Williams (clássico dos bots coreanos): compra ao passar
    abertura + k×amplitude de ontem, vende no fechamento do dia. Fade = vende no mesmo gatilho."""
    d = resample(m1, "1D")
    tgt = d.open + k * (d.high - d.low).shift(1)
    hit = d.high >= tgt
    entry = np.maximum(d.open, tgt)
    g = (d.close / entry - 1).where(hit, 0.0)
    return g.where(~hit, g - 2 * cost), (-g).where(~hit, -g - 2 * cost), g


def main():
    port = {}  # (estratégia, modo) -> lista de séries diárias por símbolo
    per_sym = []
    for sym in SYMS:
        m1 = load_1m(sym)
        fund = load_funding(sym)
        c = COST[sym]
        print(sym, len(m1), flush=True)
        for name, fn, tf in STRATS:
            b, pos = fn(m1, tf)
            pos = pos.fillna(0.0)
            for mode, p, cc in [("bruto", pos, 0.0), ("líquido", pos, c), ("fade líquido", -pos, c)]:
                r = backtest(b, p, cc, fund)
                port.setdefault((name, mode), []).append(daily(r).rename(sym))
                if mode != "bruto":
                    tpd = float(pos.diff().abs().gt(0).groupby(pos.index.floor("D")).sum().mean())
                    d = daily(r)
                    oos = d["2024":]
                    s = stats(oos, "OOS", tpd)
                    per_sym.append({"estratégia": name, "modo": mode, "ativo": sym[:-4], **{k: v for k, v in s.items() if k != "período"}})
        net, fade, gross = vol_breakout(m1, c)
        for mode, s_ in [("bruto", gross), ("líquido", net), ("fade líquido", fade)]:
            port.setdefault(("Rompimento de volatilidade k=0,5 (diário)", mode), []).append(s_.rename(sym))

    rows = []
    for (name, mode), series in port.items():
        d = pd.concat(series, axis=1).mean(axis=1)  # carteira igual entre os ativos disponíveis no dia
        for rr in split_stats(name, d.rename(None), extra={"modo": mode}):
            rows.append(rr)
    df = pd.DataFrame(rows)

    md = ["# Resultados — Day trade em cripto (dados de 1 minuto)\n",
          "Carteira igual entre BTC, ETH, SOL, DOGE e XRP (perpétuos Binance). Custos por lado: 0,06% (BTC/ETH) e 0,07% (demais) = "
          "taxa agressora VIP0 + slippage; funding real a cada 8h. `bruto` = sem custos; `fade` = sinal invertido. "
          "IS = 2020–2023; OOS = 2024–out/2026.\n"]
    md += ["## K1. Resumo OOS (2024–2026) — carteira dos 5 ativos\n"]
    piv = df[df["período"] == "OOS 2024–2026"].pivot_table(index="estratégia", columns="modo",
                                                          values=["média_mês", "sharpe"], aggfunc="first")
    summ = []
    order = [n for n, _, _ in STRATS] + ["Rompimento de volatilidade k=0,5 (diário)"]
    for n in order:
        if n not in piv.index:
            continue
        r_ = piv.loc[n]
        pct = lambda v: f"{v*100:+.1f}%"  # noqa: E731
        summ.append({"estratégia": n,
                     "bruto: média/mês": pct(r_[("média_mês", "bruto")]), "bruto: sharpe": f"{r_[('sharpe', 'bruto')]:.2f}",
                     "líquido: média/mês": pct(r_[("média_mês", "líquido")]), "líquido: sharpe": f"{r_[('sharpe', 'líquido')]:.2f}",
                     "fade: média/mês": pct(r_[("média_mês", "fade líquido")]), "fade: sharpe": f"{r_[('sharpe', 'fade líquido')]:.2f}"})
    md += [table(summ), "\n"]
    md += ["## K2. Tabela completa (carteira), IS e OOS\n", table(df.to_dict("records")), "\n"]
    ps = pd.DataFrame(per_sym)
    best = ps.sort_values("média_mês", ascending=False).head(15)
    md += ["## K3. As 15 melhores combinações estratégia×ativo no OOS (cuidado: escolher a melhor depois é viés de seleção)\n",
           table(best.to_dict("records")), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md[:6]))


if __name__ == "__main__":
    main()
