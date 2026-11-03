"""Bloco T: a "equação de memória" do preço.

O diagnóstico (S1) mostrou VR < 1 entre 4h e 3 dias (o preço reverte). Aqui:
T1. Checagem: razão de variâncias dos retornos PADRONIZADOS pela volatilidade prevista
    (remove o efeito de crashes e de volatilidade em ondas) e por bootstrap em blocos.
T2. Preditor linear ótimo (equação de memória): regressão do retorno padronizado das
    próximas 24h nos retornos padronizados passados em janelas [1–4h], [5–12h], [13–24h],
    [25–72h], [73–168h] e na tendência de 30–100 dias. Ajustado SÓ em 2020–2023 (todos os
    ativos juntos), aplicado sem mudança em 2024–2026.
T3. Versões sem ajuste (para não depender da regressão): vender a alta de 24h/72h,
    só a favor da tendência longa ("comprar a queda na tendência de alta").
Saída: research/results/mat_memoria.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intraday"))
from core import COST, SYMS, backtest, daily, load_1m, load_funding, split_stats, table  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "mat_memoria.md"
WINDOWS = [(1, 4), (5, 12), (13, 24), (25, 72), (73, 168)]
rng = np.random.default_rng(11)


def hourly(sym):
    m1 = load_1m(sym)
    h = m1.resample("1h").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    return h


def feats(h: pd.DataFrame) -> pd.DataFrame:
    lr = np.log(h.close).diff()
    sig = np.sqrt((lr ** 2).ewm(halflife=24 * 7).mean()).shift(1)  # vol prevista (conhecida antes)
    z = (lr / sig).clip(-8, 8)
    f = pd.DataFrame(index=h.index)
    for a, b in WINDOWS:
        f[f"z_{a}_{b}"] = z.shift(a - 1).rolling(b - a + 1).sum() / np.sqrt(b - a + 1)
    d = h.close.resample("1D").last()
    trend = np.sign(np.log(d / d.shift(30)) + np.log(d / d.shift(100))).reindex(h.index, method="ffill").shift(24)
    f["trend"] = trend
    fwd = np.log(h.close.shift(-24) / h.close) / (sig * np.sqrt(24))
    f["y"] = fwd.clip(-8, 8)
    f["z1"] = z
    f["sig"] = sig
    return f


def vr_std(z: np.ndarray, q: int) -> float:
    z = z[~np.isnan(z)]
    zq = np.convolve(z, np.ones(q), "valid")
    return zq.var() / (q * z.var())


def main():
    H = {s: hourly(s) for s in SYMS}
    F = {s: feats(h) for s, h in H.items()}
    md = ["# Resultados — A equação de memória do preço\n"]

    # T1: VR dos retornos padronizados + intervalo por bootstrap em blocos de 30 dias
    rows = []
    for s, f in F.items():
        z = f["z1"].values
        row = {"ativo": s[:-4]}
        for q in (4, 12, 24, 72, 168):
            v = vr_std(z, q)
            n = len(z)
            blk = 24 * 30
            boots = []
            for _ in range(200):
                starts = rng.integers(0, n - blk, n // blk)
                zb = np.concatenate([z[i:i + blk] for i in starts])
                boots.append(vr_std(rng.permutation(zb), q))  # embaralha: distribuição sob "sem memória"
            lo, hi = np.nanquantile(boots, [0.025, 0.975])
            row[f"VR {q}h"] = f"{v:.2f}" + (" ✱" if (v < lo or v > hi) else "")
        rows.append(row)
    md += ["## T1. Razão de variâncias dos retornos padronizados pela volatilidade (✱ = fora do intervalo de 95% do acaso)\n",
           table(rows), "\n"]

    # T2: regressão ajustada só no IS, aplicada no OOS
    X = pd.concat([f.assign(sym=s) for s, f in F.items()]).dropna()
    cols = [f"z_{a}_{b}" for a, b in WINDOWS] + ["trend"]
    tr = X[X.index < "2024-01-01"]
    A = np.column_stack([np.ones(len(tr)), tr[cols].values])
    beta, *_ = np.linalg.lstsq(A, tr["y"].values, rcond=None)
    resid = tr["y"].values - A @ beta
    se = np.sqrt(np.diag(np.linalg.inv(A.T @ A)) * resid.var() * 24)  # ×24: sobreposição do alvo de 24h
    coef_rows = [{"variável": n, "coeficiente": f"{b:+.4f}", "t (ajustado)": f"{b/e:+.1f}"}
                 for n, b, e in zip(["constante"] + cols, beta, se)]
    md += ["## T2. Equação de memória (ajustada em 2020–2023, todos os ativos)\n",
           "E[retorno 24h / σ] = soma dos coeficientes × retornos passados padronizados. Coeficiente negativo = reversão.\n",
           table(coef_rows), "\n"]

    port = {}
    for s, f in F.items():
        h, fund = H[s], load_funding(s)
        ff = f.dropna(subset=cols)
        pred = pd.Series(np.column_stack([np.ones(len(ff)), ff[cols].values]) @ beta, index=ff.index)
        scale = pred[:"2023"].std()
        variants = {
            "Equação de memória (regressão IS)": (pred / scale).clip(-1, 1),
            "Vende a alta de 24h (−z 24h)": (-f["z_13_24"] - f["z_5_12"] - f["z_1_4"]).div(3).clip(-1, 1),
            "Vende a alta de 72h (−z 25–72h)": (-f["z_25_72"] / 2).clip(-1, 1),
            "Compra queda de 72h só na tendência de alta (e vice-versa)":
                ((-f["z_25_72"] / 2).clip(-1, 1)).where(np.sign(-f["z_25_72"]) == f["trend"], 0.0),
        }
        for name, pos in variants.items():
            pos = pos.reindex(h.index).fillna(0.0).rolling(24, min_periods=1).mean()  # 24 tranches horárias
            port.setdefault(name, []).append(daily(backtest(h, pos, COST[s], fund)).rename(s))
    rows = []
    for name, ser in port.items():
        d = pd.concat(ser, axis=1).mean(axis=1)
        rows += split_stats(name, d.rename(None))
    md += ["## T3. Estratégias de reversão (carteira dos 5 ativos, custos + funding, posição suavizada em 24 tranches)\n",
           table(rows), "\n"]
    OUT.write_text("\n".join(md))
    pd.concat({k: pd.concat(v, axis=1).mean(axis=1) for k, v in port.items()}, axis=1).to_parquet("/tmp/claude-0/mat_memoria.parquet")
    print("\n".join(md))


if __name__ == "__main__":
    main()
