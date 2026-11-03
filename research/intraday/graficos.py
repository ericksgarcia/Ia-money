"""Gráficos do estudo intradiário (lê os resultados já gerados)."""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def custos():
    txt = (RES / "intraday_daytrade_cripto.md").read_text()
    block = txt.split("## K1")[1].split("## K2")[0]
    rows = []
    for ln in block.splitlines():
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) == 7 and re.match(r"[+-]\d", cells[1]):
            rows.append((cells[0], *[float(cells[i].rstrip("%")) for i in (1, 3, 5)]))
    df = pd.DataFrame(rows, columns=["estratégia", "bruto", "líquido", "fade líquido"]).set_index("estratégia")
    df = df.sort_values("bruto")
    ax = df.plot.barh(figsize=(10, 8), width=0.8, color=["#9aa5b1", "#d1495b", "#edae49"])
    ax.axvline(5, color="green", ls="--", lw=1)
    ax.text(5.2, -0.6, "meta 5%/mês", color="green", fontsize=8)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("Retorno médio mensal OOS 2024–2026 (%) — carteira BTC/ETH/SOL/DOGE/XRP")
    ax.set_title("Day trade popular em cripto: antes dos custos ≈ 0;\ndepois dos custos perde — e o fade (fazer o contrário) também")
    ax.set_xlim(-60, 10)
    plt.tight_layout()
    plt.savefig(RES / "g_intraday_custos.png", dpi=130)
    plt.close()


def combo():
    df = pd.read_parquet("/tmp/claude-0/meta5_series.parquet")
    fig, (a, b) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    for c in df.columns:
        eq = (1 + df[c]).cumprod()
        lw = 2.4 if c.startswith("Combinação") else 1.1
        a.plot(eq.index, eq, lw=lw, label=c)
        if c.startswith("Combinação"):
            b.plot(eq.index, (eq / eq.cummax() - 1) * 100, lw=1.5, label="Combinação 1×")
            eq3 = (1 + 2.8 * df[c]).cumprod()
            a.plot(eq3.index, eq3, lw=1.6, ls="--", color="black", label="Combinação 2,8× (média ≈ 5%/mês)")
            b.plot(eq3.index, (eq3 / eq3.cummax() - 1) * 100, lw=1.2, ls="--", color="black", label="Combinação 2,8×")
    a.set_yscale("log"); a.legend(fontsize=8, loc="upper left"); a.grid(alpha=0.3)
    a.set_title("Estratégias sobreviventes (sinais com 1h de atraso extra) e combinação, 2022–2026")
    a.axvline(pd.Timestamp("2024-01-01"), color="gray", ls=":")
    a.text(pd.Timestamp("2024-01-15"), a.get_ylim()[0] * 1.05, "fora da amostra →", fontsize=8, color="gray")
    b.set_ylabel("Drawdown %"); b.grid(alpha=0.3); b.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(RES / "g_intraday_combinacao.png", dpi=130)
    plt.close()


if __name__ == "__main__":
    custos()
    combo()
    print("ok")
