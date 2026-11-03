# Resultados — A equação de memória do preço

## T1. Razão de variâncias dos retornos padronizados pela volatilidade (✱ = fora do intervalo de 95% do acaso)

| ativo | VR 4h | VR 12h | VR 24h | VR 72h | VR 168h |
|---|---|---|---|---|---|
| BTC | 0.99 | 1.01 | 1.06 ✱ | 1.13 ✱ | 1.25 ✱ |
| ETH | 1.00 | 1.02 | 1.06 ✱ | 1.15 ✱ | 1.24 ✱ |
| SOL | 0.97 ✱ | 0.97 | 1.01 | 1.07 | 1.16 ✱ |
| DOGE | 0.95 ✱ | 0.96 ✱ | 1.00 | 1.06 | 1.14 ✱ |
| XRP | 0.96 ✱ | 0.95 ✱ | 0.98 | 1.03 | 1.14 ✱ |


## T2. Equação de memória (ajustada em 2020–2023, todos os ativos)

E[retorno 24h / σ] = soma dos coeficientes × retornos passados padronizados. Coeficiente negativo = reversão.

| variável | coeficiente | t (ajustado) |
|---|---|---|
| constante | +0.0336 | +2.5 |
| z_1_4 | +0.0119 | +0.9 |
| z_5_12 | +0.0105 | +0.8 |
| z_13_24 | +0.0054 | +0.4 |
| z_25_72 | +0.0691 | +5.2 |
| z_73_168 | +0.0126 | +1.0 |
| trend | +0.0191 | +1.4 |


## T3. Estratégias de reversão (carteira dos 5 ativos, custos + funding, posição suavizada em 24 tranches)

| estratégia | período | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês |
|---|---|---|---|---|---|---|---|---|
| Equação de memória (regressão IS) | total | 32.5% | 0.83 | -66.9% | 3.9% | -0.1% | 26% | -20.4% |
| Equação de memória (regressão IS) | IS 2020–2023 | 74.1% | 1.32 | -48.1% | 6.4% | 0.0% | 31% | -19.7% |
| Equação de memória (regressão IS) | OOS 2024–2026 | -9.9% | -0.05 | -66.9% | 0.3% | -0.8% | 18% | -20.4% |
| Vende a alta de 24h (−z 24h) | total | -22.4% | -0.54 | -84.3% | -1.7% | -0.8% | 22% | -30.4% |
| Vende a alta de 24h (−z 24h) | IS 2020–2023 | -20.7% | -0.37 | -68.1% | -1.5% | -0.4% | 25% | -30.4% |
| Vende a alta de 24h (−z 24h) | OOS 2024–2026 | -24.7% | -0.91 | -62.0% | -2.0% | -2.1% | 18% | -24.0% |
| Vende a alta de 72h (−z 25–72h) | total | -28.5% | -0.86 | -91.6% | -2.5% | -2.1% | 9% | -31.9% |
| Vende a alta de 72h (−z 25–72h) | IS 2020–2023 | -36.7% | -1.06 | -85.0% | -3.4% | -3.1% | 6% | -31.9% |
| Vende a alta de 72h (−z 25–72h) | OOS 2024–2026 | -15.0% | -0.49 | -46.5% | -1.1% | -1.0% | 12% | -19.3% |
| Compra queda de 72h só na tendência de alta (e vice-versa) | total | -0.4% | 0.06 | -32.9% | 0.1% | 0.0% | 7% | -10.9% |
| Compra queda de 72h só na tendência de alta (e vice-versa) | IS 2020–2023 | -0.3% | 0.07 | -27.0% | 0.1% | 0.0% | 8% | -10.0% |
| Compra queda de 72h só na tendência de alta (e vice-versa) | OOS 2024–2026 | -0.5% | 0.04 | -13.9% | 0.0% | 0.5% | 6% | -10.9% |

