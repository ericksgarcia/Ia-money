"""Bloco S: a estrutura matemática do preço.

S1. Razão de variâncias de Lo-MacKinlay, VR(q) = Var(r_q) / (q·Var(r_1)), de q = 2 min a 14 dias.
    VR < 1 → o preço reverte nessa escala; VR > 1 → tem tendência (memória positiva);
    z robusto a heterocedasticidade. Equivale a medir o expoente de Hurst escala a escala:
    H(q) ≈ 0,5 + log(VR(q)) / (2·log q).
S2. Espectro de potência (Fourier) dos retornos horários e dos retornos absolutos
    (volatilidade), com limiar de significância por permutação: existem ciclos reais?
S3. Memória da volatilidade: autocorrelação de |r| e expoente de Hurst da volatilidade.

Saída: research/results/mat_diag.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intraday"))
from core import SYMS, load_1m, table  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "mat_diag.md"
QS = [2, 5, 15, 30, 60, 240, 720, 1440, 4320, 10080, 20160]
rng = np.random.default_rng(7)


def vr_test(r: np.ndarray, q: int):
    """Lo & MacKinlay (1988) com estatística z* robusta a heterocedasticidade."""
    r = r[~np.isnan(r)]
    n = len(r)
    mu = r.mean()
    d = r - mu
    s1 = (d @ d) / (n - 1)
    rq = np.convolve(r, np.ones(q), "valid")
    m = q * (n - q + 1) * (1 - q / n)
    sq = ((rq - q * mu) ** 2).sum() / m
    vr = sq / s1
    # variância assintótica robusta (soma dos delta_j)
    d2 = d ** 2
    denom = (d2.sum()) ** 2
    theta = 0.0
    for j in range(1, q):
        delta = n * (d2[j:] * d2[:-j]).sum() / denom
        theta += (2 * (q - j) / q) ** 2 * delta
    zs = (vr - 1) / np.sqrt(theta) if theta > 0 else np.nan
    return vr, zs


def vr_fast(r: np.ndarray, q: int):
    """Para q grande: z homocedástico (o robusto é caro e muito parecido em amostras longas)."""
    r = r[~np.isnan(r)]
    n = len(r)
    mu = r.mean()
    s1 = r.var(ddof=1)
    rq = np.convolve(r, np.ones(q), "valid")
    m = q * (n - q + 1) * (1 - q / n)
    vr = ((rq - q * mu) ** 2).sum() / m / s1
    phi = 2 * (2 * q - 1) * (q - 1) / (3 * q * n)
    return vr, (vr - 1) / np.sqrt(phi)


def main():
    md = ["# Resultados — A estrutura matemática do preço\n"]
    vr_rows, spec_rows, vol_rows = [], [], []
    for sym in SYMS:
        m1 = load_1m(sym)
        lr = np.log(m1.close).diff()
        for per, sl in [("IS 2020–2023", slice(None, "2023")), ("OOS 2024–2026", slice("2024", None))]:
            r = lr[sl].values
            row = {"ativo": sym[:-4], "período": per}
            for q in QS:
                vr, zs = (vr_test(r, q) if q <= 60 else vr_fast(r, q))
                h = 0.5 + np.log(vr) / (2 * np.log(q))
                star = "**" if abs(zs) > 3 else ""
                row[f"{q}m" if q < 60 else (f"{q//60}h" if q < 1440 else f"{q//1440}d")] = f"{star}{vr:.2f}{star}"
            vr_rows.append(row)
        # espectro dos retornos horários e da volatilidade
        h1 = np.log(m1.close.resample("1h").last()).diff().dropna()
        for label, x in [("retornos", h1.values), ("|retornos| (volatilidade)", np.abs(h1.values))]:
            x = x - x.mean()
            p = np.abs(np.fft.rfft(x)) ** 2
            f = np.fft.rfftfreq(len(x), d=1.0)
            mask = (f > 1 / (24 * 30)) & (f < 0.5)  # períodos entre 2h e 30 dias
            perm_max = []
            for _ in range(30):
                xs = rng.permutation(x)
                pp = np.abs(np.fft.rfft(xs)) ** 2
                perm_max.append(pp[mask].max())
            thr = np.quantile(perm_max, 0.95)
            idx = np.where(mask & (p > thr))[0]
            top = sorted(idx, key=lambda i: -p[i])[:5]
            spec_rows.append({"ativo": sym[:-4], "série": label,
                              "ciclos significativos (período em horas)": ", ".join(f"{1/f[i]:.1f}h" for i in top) or "nenhum",
                              "potência do maior pico / limiar 95%": f"{p[mask].max()/thr:.2f}"})
        a = np.abs(h1)
        vol_rows.append({"ativo": sym[:-4], **{f"autocorr |r| lag {k}h": f"{a.autocorr(k):.2f}" for k in (1, 24, 168, 720)},
                         "autocorr r lag 1h": f"{h1.autocorr(1):+.3f}"})
        print(sym, flush=True)
    md += ["## S1. Razão de variâncias por escala (1 = passeio aleatório; <1 reversão; >1 tendência)\n",
           "Negrito = |z| > 3. Expoente de Hurst local ≈ 0,5 + ln(VR)/(2·ln q).\n", table(vr_rows), "\n",
           "## S2. Ciclos de Fourier (retornos horários, períodos de 2h a 30 dias, limiar por 30 permutações)\n",
           table(spec_rows), "\n",
           "## S3. Memória da volatilidade vs memória do retorno\n", table(vol_rows), "\n"]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
