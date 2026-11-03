# Resultados — Mineração de equações com controle de falsas descobertas

18 descritores, alvo = retorno 24h / σ. Seleção só com 2020–2023 (Benjamini-Hochberg 10%). Aprovados: **hurst_local, assimetria_7d, compressao_range, dist_max_30d, dist_min_30d, volume_anormal, desequilibrio_agressor, vol_relativa**.

## X1. Poder preditivo de cada descritor (IS) e o que aconteceu depois (OOS)

| descritor | IS: decil10 − decil1 (σ) | IS t | monotonia (Spearman) | OOS: decil10 − decil1 (σ) | OOS t | aprovado (FDR 10%) |
|---|---|---|---|---|---|---|
| entropia_1m | +0.009 | 0.16 | 0.18 | -0.026 | -0.38 |  |
| entropia_1h | +0.049 | 0.85 | 0.39 | +0.004 | 0.05 |  |
| hurst_local | -0.127 | -2.11 | -0.76 | +0.015 | 0.22 | SIM |
| curvatura | +0.052 | 0.80 | 0.28 | -0.042 | -0.62 |  |
| velocidade | +0.056 | 0.81 | 0.32 | +0.148 | 2.09 |  |
| wavelet_fino_grosso | -0.062 | -1.10 | -0.90 | +0.055 | 0.87 |  |
| assimetria_7d | +0.139 | 2.45 | 0.84 | -0.009 | -0.11 | SIM |
| curtose_7d | -0.095 | -1.78 | -0.55 | +0.014 | 0.16 |  |
| compressao_range | +0.144 | 2.24 | 0.94 | +0.161 | 2.23 | SIM |
| eficiencia_kaufman | +0.056 | 0.92 | 0.77 | +0.081 | 1.22 |  |
| autocorr_local | -0.043 | -0.81 | -0.04 | -0.206 | -2.56 |  |
| dist_max_30d | +0.221 | 3.21 | 0.85 | +0.208 | 2.69 | SIM |
| dist_min_30d | +0.202 | 3.00 | 0.94 | +0.165 | 2.35 | SIM |
| vol_da_vol | +0.031 | 0.54 | 0.22 | +0.241 | 3.34 |  |
| frac_horas_alta | +0.025 | 0.40 | 0.48 | +0.248 | 2.50 |  |
| volume_anormal | +0.186 | 2.95 | 1.00 | +0.190 | 2.62 | SIM |
| desequilibrio_agressor | +0.116 | 2.02 | 0.09 | +0.212 | 2.02 | SIM |
| vol_relativa | +0.131 | 2.07 | 0.95 | +0.161 | 2.27 | SIM |


## X2. Estratégia com o sinal composto (carteira dos 5 ativos, custos + funding)

| estratégia | período | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês |
|---|---|---|---|---|---|---|---|---|
| Sinal composto dos descritores aprovados | total | 51.6% | 1.49 | -37.8% | 4.2% | 0.3% | 34% | -12.5% |
| Sinal composto dos descritores aprovados | IS 2020–2023 | 86.9% | 1.96 | -23.5% | 6.2% | 2.0% | 44% | -12.5% |
| Sinal composto dos descritores aprovados | OOS 2024–2026 | 12.7% | 0.61 | -37.8% | 1.5% | -0.2% | 21% | -9.8% |

