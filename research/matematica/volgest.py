"""Bloco Y: a parte previsível do preço é a volatilidade — usá-la para dimensionar posições.

Y1. Modelo HAR (Corsi 2009) para a volatilidade realizada diária (de retornos de 5 min):
    log RV(t+1) = a + b_d·log RV_d + b_w·log RV_semana + b_m·log RV_mês.
    Ajuste até 2023, previsão 2024–2026: R² fora da amostra vs "amanhã = hoje".
Y2. Gestão por volatilidade (Moreira & Muir 2017): exposição_t = alvo / σ̂_t (limitada),
    com σ̂ prevista só com dados até t−1, aplicada a cada estratégia sobrevivente e à combinação.
Y3. Nova combinação (inclusão de novas estratégias decidida SÓ pelo desempenho antes de 2024),
    alavancagem para 5%/mês e Monte Carlo.
Saída: research/results/mat_volgest.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intraday"))
from core import SYMS, load_1m, monthly, stats, table  # noqa: E402
from meta5 import simulate  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "mat_volgest.md"
EXTRA = {  # séries candidatas de estudos 3 (incluídas só se passarem no critério IS)
    "Ímã de liquidação": ("/tmp/claude-0/mat_liquidez.parquet", "a favor do ímã"),
    "Mineração (composto)": ("/tmp/claude-0/mat_mineracao.parquet", "mineracao"),
    "PCA/OU stat-arb": ("/tmp/claude-0/mat_statarb.parquet", "pca"),
}


def har():
    rows = []
    for s in SYMS:
        m1 = load_1m(s)
        r5 = np.log(m1.close.resample("5min").last()).diff().dropna()
        rv = (r5 ** 2).groupby(r5.index.floor("D")).sum()
        lrv = np.log(rv[rv > 0])
        X = pd.DataFrame({"d": lrv, "w": lrv.rolling(7).mean(), "m": lrv.rolling(30).mean()}).shift(1)
        df = pd.concat([lrv.rename("y"), X], axis=1, sort=True).dropna()
        tr, te = df[:"2023"], df["2024":]
        A = np.column_stack([np.ones(len(tr)), tr[["d", "w", "m"]].values])
        b, *_ = np.linalg.lstsq(A, tr.y.values, rcond=None)
        pred = np.column_stack([np.ones(len(te)), te[["d", "w", "m"]].values]) @ b
        sse = ((te.y - pred) ** 2).sum()
        sst = ((te.y - te.y.mean()) ** 2).sum()
        naive = ((te.y - te.d) ** 2).sum()
        rows.append({"ativo": s[:-4], "b_dia": f"{b[1]:.2f}", "b_semana": f"{b[2]:.2f}", "b_mês": f"{b[3]:.2f}",
                     "R² OOS (log RV)": f"{1 - sse/sst:.2f}", "erro vs 'amanhã = hoje'": f"{sse/naive*100:.0f}%"})
    return rows


def vol_manage(r: pd.Series, target_ann=0.20, hl=20, cap=3.0) -> pd.Series:
    sig = np.sqrt((r ** 2).ewm(halflife=hl, min_periods=30).mean()).shift(1) * np.sqrt(365)
    w = (target_ann / sig).clip(upper=cap)
    return (r * w).dropna()


def main():
    df = pd.read_parquet("/tmp/claude-0/meta5_series.parquet")
    base = [c for c in df.columns if not c.startswith("Combinação")]
    S = df[base].copy()
    incl = []
    for name, (path, col) in EXTRA.items():
        p = Path(path)
        if not p.exists():
            continue
        x = pd.read_parquet(p)[col].reindex(S.index)
        pre = x[:"2023"].dropna()
        st = stats(pre)
        ok = bool(st) and st["sharpe"] > 0.5
        incl.append({"candidata": name, "Sharpe até 2023": round(st.get("sharpe", np.nan), 2) if st else "—",
                     "incluída?": "sim" if ok else "não"})
        if ok:
            S[name] = x.fillna(0.0)
    md = ["# Resultados — Volatilidade prevista e gestão de risco\n",
          "## Y1. A volatilidade é previsível (modelo HAR, ajuste até 2023, teste 2024–2026)\n", table(har()), "\n",
          "## Y3a. Critério de inclusão de novas estratégias (decidido só com dados até 2023: Sharpe > 0,5)\n",
          table(incl) if incl else "(nenhuma candidata)", "\n"]

    VM = pd.DataFrame({c: vol_manage(S[c]) for c in S.columns})
    is_ = S[:"2023"]
    w = (1 / is_.std()) / (1 / is_.std()).sum()
    combo = (S * w).sum(axis=1)
    combo_vm = vol_manage(combo, target_ann=0.15)
    rows = []
    for name, r in list(S.items()) + [("Combinação", combo)]:
        for lab, x in [("sem gestão", r), ("com gestão de vol.", vol_manage(r) if name != "Combinação" else combo_vm)]:
            for per, sub in [("até 2023", x[:"2023"]), ("OOS 2024–2026", x["2024":])]:
                st = stats(sub, per)
                rows.append({"estratégia": name, "versão": lab, **st})
    md += ["## Y2. Efeito da gestão por volatilidade (exposição = alvo / σ prevista)\n", table(rows), "\n"]

    md += ["## Y3b. Meta de 5% ao mês com a combinação gerida por volatilidade\n"]
    r = combo_vm["2024":]
    m = monthly(r).mean()
    levs = sorted({1.0, 2.0, 3.0, round(0.05 / m, 1) if m > 0 else 1.0})
    md += [f"Pesos (estimados até 2023): " + ", ".join(f"{k} {v*100:.0f}%" for k, v in w.items()) + ".\n",
           f"Média mensal OOS sem alavancagem: {m*100:+.2f}%.\n", table([simulate(r, L) for L in levs]), "\n"]
    full = combo_vm
    for L in (1.0, round(0.05 / m, 1) if m > 0 else 1.0):
        x = L * full
        y = (1 + x).groupby(x.index.year).prod() - 1
        eq = (1 + x).cumprod()
        md.append(f"- {L:.1f}×: " + ", ".join(f"{k}: {v*100:+.0f}%" for k, v in y.items())
                  + f" · queda máx. {(eq/eq.cummax()-1).min()*100:.0f}% · meses ≥5%: {(monthly(x) >= 0.05).mean()*100:.0f}%\n")
    OUT.write_text("\n".join(md))
    pd.DataFrame({"combo": combo, "combo_vm": combo_vm}).to_parquet("/tmp/claude-0/mat_combo.parquet")
    print("\n".join(md))


if __name__ == "__main__":
    main()
