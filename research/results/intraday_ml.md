# Resultados — Machine learning (LightGBM, walk-forward mensal)

25 variáveis, 193,560 previsões horárias fora da amostra (jun/2022–out/2026), 5 ativos.

Correlação de postos (IC) média entre previsão e retorno 24h: **0.029** (meses com IC > 0: 62%).

| estratégia | período | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês |
|---|---|---|---|---|---|---|---|---|
| LightGBM · posição = previsão (±1) | total | 6.2% | 0.36 | -31.8% | 0.7% | 1.5% | 34% | -13.8% |
| LightGBM · posição = previsão (±1) | 2022-06–2023 (fora da amostra) | -2.7% | 0.01 | -28.9% | -0.0% | -0.0% | 32% | -13.8% |
| LightGBM · posição = previsão (±1) | 2024–2026 (fora da amostra) | 11.5% | 0.52 | -27.3% | 1.2% | 2.2% | 35% | -12.6% |
| LightGBM · só sinais fortes (|z|>1) | total | 4.9% | 0.38 | -21.0% | 0.5% | 0.6% | 13% | -8.0% |
| LightGBM · só sinais fortes (|z|>1) | 2022-06–2023 (fora da amostra) | 2.6% | 0.26 | -17.6% | 0.3% | 0.9% | 11% | -8.0% |
| LightGBM · só sinais fortes (|z|>1) | 2024–2026 (fora da amostra) | 6.2% | 0.44 | -16.3% | 0.6% | 0.4% | 15% | -7.3% |


## Importância das variáveis (ganho acumulado)

| variável | importância_% |
|---|---|
| btc_z_acc | 10.9% |
| vol_24 | 10.3% |
| top_lvl | 9.3% |
| vol_ratio | 8.8% |
| dow | 8.0% |
| acc_lvl | 7.6% |
| z_funding | 6.1% |
| z_top | 5.9% |
| r_168 | 5.6% |
| z_acc | 5.1% |
| funding | 4.2% |
| btc_r_24 | 3.9% |
| d_acc_24 | 3.5% |
| r_72 | 3.3% |
| d_top_24 | 3.0% |

