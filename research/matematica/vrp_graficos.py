"""Prêmio de risco de variância (DVOL × volatilidade realizada) e gráficos do estudo 3.

DVOL (volatilidade implícita de 30 dias da Deribit) vem do repositório JackREscowitz/pvol
(backend/data/history.json, 190 dias: jul/2025–fev/2026), copiado para <DATA>/dvol/pvol_history.json.
Saídas: research/results/mat_vrp.md, g_mat_vr.png, g_mat_mineracao.png
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intraday"))
from core import DATA, SYMS, load_1m  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def vrp():
    d = pd.DataFrame(json.load(open(DATA / "dvol/pvol_history.json")))
    d["date"] = pd.to_datetime(d["date"])
    d = d.set_index("date").sort_index()
    m1 = load_1m("BTCUSDT")
    r5 = np.log(m1.close.resample("5min").last()).diff().dropna()
    rv_d = (r5 ** 2).groupby(r5.index.floor("D")).sum()
    rv_fwd30 = np.sqrt(rv_d[::-1].rolling(30).sum()[::-1].shift(-1) * 365 / 30)
    x = pd.concat([d["dvol"], rv_fwd30.rename("rv30")], axis=1, sort=True).dropna()
    pnl = (x.dvol ** 2 - x.rv30 ** 2) / (2 * x.dvol) * (30 / 365)
    md = ["# Resultados — Prêmio de risco de variância do BTC (DVOL vs realizada)\n",
          f"{len(x)} datas ({x.index.min():%Y-%m-%d} → {x.index.max():%Y-%m-%d}).\n",
          f"- DVOL médio: {x.dvol.mean()*100:.1f}%; volatilidade realizada nos 30 dias seguintes: {x.rv30.mean()*100:.1f}%.\n",
          f"- Prêmio médio (implícita − realizada): {(x.dvol - x.rv30).mean()*100:+.1f} pontos; implícita > realizada em {((x.dvol - x.rv30) > 0).mean()*100:.0f}% das datas.\n",
          f"- Vendido em variância por 30 dias (notional de vega): média {pnl.mean()*100:+.2f}%, pior {pnl.min()*100:+.2f}%, melhor {pnl.max()*100:+.2f}%.\n",
          "Amostra curta (≈ 6 meses independentes): serve só como indicação.\n"]
    (RES / "mat_vrp.md").write_text("\n".join(md))
    print("\n".join(md))


def vr_chart():
    qs = [1, 2, 4, 8, 12, 24, 48, 72, 120, 168]
    raw, std = [], []
    for s in SYMS:
        h = load_1m(s).close.resample("1h").last().dropna()
        lr = np.log(h).diff().dropna()
        sig = np.sqrt((lr ** 2).ewm(halflife=24 * 7).mean()).shift(1)
        z = (lr / sig).clip(-8, 8).dropna()
        for arr, out in [(lr.values, raw), (z.values, std)]:
            out.append([np.convolve(arr, np.ones(q), "valid").var() / (q * arr.var()) for q in qs])
    raw, std = np.mean(raw, axis=0), np.mean(std, axis=0)
    plt.figure(figsize=(9, 5))
    plt.plot(qs, raw, "o-", label="retornos brutos (parece reversão)")
    plt.plot(qs, std, "o-", label="retornos ÷ volatilidade prevista (é momentum)")
    plt.axhline(1, color="gray", ls="--", lw=1)
    plt.xscale("log")
    plt.xticks(qs, [f"{q}h" for q in qs])
    plt.ylabel("Razão de variâncias VR(q)  (1 = passeio aleatório)")
    plt.title("A 'reversão à média' em cripto é ilusão da volatilidade\n(média dos 5 perpétuos, 2020–2026)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(RES / "g_mat_vr.png", dpi=130)
    plt.close()


def mining_chart():
    txt = (RES / "mat_mineracao.md").read_text()
    rows = []
    for ln in txt.splitlines():
        c = [x.strip() for x in ln.strip("|").split("|")]
        if len(c) == 7 and re.match(r"^-?\d", c[2] or "x"):
            rows.append((c[0], float(c[2]), float(c[5]), c[6] == "SIM"))
    df = pd.DataFrame(rows, columns=["d", "t_is", "t_oos", "ok"])
    plt.figure(figsize=(8, 7))
    for ok, col, lab in [(True, "#d1495b", "aprovado no IS (FDR 10%)"), (False, "#9aa5b1", "reprovado no IS")]:
        s = df[df.ok == ok]
        plt.scatter(s.t_is, s.t_oos, c=col, s=60, label=lab)
        for _, r in s.iterrows():
            plt.annotate(r.d, (r.t_is, r.t_oos), fontsize=7, xytext=(3, 3), textcoords="offset points")
    plt.axhline(0, color="gray", lw=0.8)
    plt.axvline(0, color="gray", lw=0.8)
    plt.plot([-4, 4], [-4, 4], ls=":", color="gray")
    plt.xlabel("t-estatística 2020–2023 (seleção)")
    plt.ylabel("t-estatística 2024–2026 (teste)")
    plt.title("Descritores matemáticos: quem se repetiu fora da amostra")
    plt.legend(fontsize=8)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(RES / "g_mat_mineracao.png", dpi=130)
    plt.close()


if __name__ == "__main__":
    vrp()
    vr_chart()
    mining_chart()
