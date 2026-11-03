# Resultados — Posicionamento da multidão e microestrutura

Dados: métricas de 5 min da Binance (open interest, razão long/short das contas e dos top traders, fluxo agressor) e candles de 1 min dos perpétuos. Sinais calculados no fechamento de cada hora; versão operável segura 24h. IS até 2023, OOS 2024–2026. Retornos futuros já com o sinal aplicado (positivo = o sinal acertou).

## L1. O que o varejo faz

A razão long/short das contas mede quantas contas estão compradas vs vendidas (cada conta pesa igual, então é dominada pelo varejo).

| ativo | % contas compradas (média) | corr(Δ long/short 24h, retorno 24h) | corr(Δ long/short 24h, retorno PRÓXIMAS 24h) | corr(top traders Δ24h, retorno próximas 24h) |
|---|---|---|---|---|
| BTC | 59% | -0.49 | -0.05 | -0.01 |
| ETH | 65% | -0.57 | -0.04 | -0.02 |
| SOL | 70% | -0.45 | -0.04 | -0.01 |
| DOGE | 75% | -0.34 | 0.00 | 0.03 |
| XRP | 73% | -0.48 | -0.00 | -0.02 |


## L2. Sinais de posicionamento — estratégia operável (carteira dos 5 ativos, segura 24h, custos + funding)

| estratégia | modo | período | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês |
|---|---|---|---|---|---|---|---|---|---|
| Contra o varejo: contas muito compradas → vende (e vice-versa) | líquido | total | 65.7% | 1.58 | -25.2% | 4.8% | 3.3% | 43% | -16.1% |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | líquido | IS 2020–2023 | 110.0% | 2.00 | -24.8% | 6.9% | 4.9% | 49% | -11.9% |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | líquido | OOS 2024–2026 | 25.3% | 0.94 | -25.2% | 2.3% | 1.5% | 35% | -16.1% |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | fade líquido | total | -56.0% | -2.20 | -99.4% | -6.0% | -5.6% | 15% | -31.9% |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | fade líquido | IS 2020–2023 | -65.8% | -2.52 | -97.5% | -7.7% | -6.9% | 15% | -31.9% |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | fade líquido | OOS 2024–2026 | -40.9% | -1.76 | -78.8% | -4.0% | -4.6% | 15% | -19.1% |
| A favor dos top traders: posições compradas → compra | líquido | total | -1.9% | 0.08 | -46.4% | 0.1% | 0.0% | 19% | -28.2% |
| A favor dos top traders: posições compradas → compra | líquido | IS 2020–2023 | -3.0% | 0.06 | -40.7% | 0.1% | 0.0% | 20% | -28.2% |
| A favor dos top traders: posições compradas → compra | líquido | OOS 2024–2026 | -0.6% | 0.11 | -39.3% | 0.2% | -1.1% | 18% | -14.7% |
| A favor dos top traders: posições compradas → compra | fade líquido | total | -22.2% | -0.71 | -81.8% | -1.8% | -0.5% | 12% | -25.2% |
| A favor dos top traders: posições compradas → compra | fade líquido | IS 2020–2023 | -19.6% | -0.55 | -57.2% | -1.5% | 0.0% | 10% | -13.6% |
| A favor dos top traders: posições compradas → compra | fade líquido | OOS 2024–2026 | -25.1% | -0.94 | -64.8% | -2.1% | -0.9% | 15% | -25.2% |
| Top traders compram enquanto varejo vende | líquido | total | 31.8% | 1.06 | -32.8% | 2.5% | 0.3% | 29% | -11.5% |
| Top traders compram enquanto varejo vende | líquido | IS 2020–2023 | 34.1% | 1.05 | -32.8% | 2.7% | 0.0% | 32% | -11.5% |
| Top traders compram enquanto varejo vende | líquido | OOS 2024–2026 | 29.2% | 1.09 | -26.7% | 2.4% | 1.3% | 26% | -8.9% |
| Top traders compram enquanto varejo vende | fade líquido | total | -41.9% | -1.65 | -96.8% | -4.1% | -3.2% | 9% | -27.0% |
| Top traders compram enquanto varejo vende | fade líquido | IS 2020–2023 | -42.8% | -1.54 | -85.4% | -4.2% | -3.2% | 5% | -27.0% |
| Top traders compram enquanto varejo vende | fade líquido | OOS 2024–2026 | -40.8% | -1.82 | -78.7% | -4.0% | -3.5% | 15% | -20.9% |
| Contra o fluxo agressor extremo | líquido | total | -24.0% | -1.28 | -83.8% | -2.1% | -1.6% | 5% | -16.9% |
| Contra o fluxo agressor extremo | líquido | IS 2020–2023 | -25.9% | -1.17 | -68.4% | -2.2% | -0.7% | 7% | -16.9% |
| Contra o fluxo agressor extremo | líquido | OOS 2024–2026 | -21.8% | -1.53 | -54.8% | -2.0% | -2.6% | 3% | -10.3% |
| Contra o fluxo agressor extremo | fade líquido | total | -2.6% | -0.03 | -38.1% | -0.1% | -0.6% | 13% | -17.0% |
| Contra o fluxo agressor extremo | fade líquido | IS 2020–2023 | 0.2% | 0.12 | -28.2% | 0.2% | -1.0% | 22% | -17.0% |
| Contra o fluxo agressor extremo | fade líquido | OOS 2024–2026 | -5.8% | -0.31 | -25.1% | -0.4% | -0.2% | 3% | -10.1% |
| Cascata de liquidação: queda forte + OI despenca → compra | líquido | total | 23.9% | 0.88 | -45.2% | 2.2% | 0.7% | 24% | -20.5% |
| Cascata de liquidação: queda forte + OI despenca → compra | líquido | IS 2020–2023 | 30.5% | 0.97 | -45.2% | 2.8% | 0.5% | 32% | -20.5% |
| Cascata de liquidação: queda forte + OI despenca → compra | líquido | OOS 2024–2026 | 16.6% | 0.77 | -29.9% | 1.5% | 1.0% | 15% | -11.6% |
| Cascata de liquidação: queda forte + OI despenca → compra | fade líquido | total | -34.1% | -1.34 | -92.5% | -3.0% | -1.8% | 8% | -39.0% |
| Cascata de liquidação: queda forte + OI despenca → compra | fade líquido | IS 2020–2023 | -39.1% | -1.41 | -81.2% | -3.5% | -1.3% | 10% | -39.0% |
| Cascata de liquidação: queda forte + OI despenca → compra | fade líquido | OOS 2024–2026 | -27.5% | -1.29 | -61.4% | -2.4% | -2.2% | 6% | -21.7% |
| Contra o funding extremo | líquido | total | 5.0% | 0.31 | -46.4% | 0.7% | 0.4% | 21% | -30.5% |
| Contra o funding extremo | líquido | IS 2020–2023 | 21.9% | 0.70 | -28.6% | 1.9% | 1.3% | 24% | -12.3% |
| Contra o funding extremo | líquido | OOS 2024–2026 | -11.9% | -0.34 | -46.4% | -0.8% | 0.1% | 18% | -30.5% |
| Contra o funding extremo | fade líquido | total | -24.5% | -0.68 | -83.6% | -2.0% | -1.4% | 11% | -18.4% |
| Contra o funding extremo | fade líquido | IS 2020–2023 | -35.5% | -0.98 | -78.7% | -3.3% | -2.4% | 10% | -18.4% |
| Contra o funding extremo | fade líquido | OOS 2024–2026 | -9.0% | -0.22 | -34.2% | -0.5% | -0.8% | 12% | -15.7% |


## L2b. Estudo de eventos por ativo (retorno futuro médio na direção do sinal)

| sinal | ativo | período | eventos | ret_1h | ret_4h | ret_24h | t_24h | ret_k_min |
|---|---|---|---|---|---|---|---|---|
| Contra o varejo: contas muito compradas → vende (e vice-versa) | BTC | IS | 3284 | +0.06% | +0.24% | +0.80% | 2.51 |  |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | BTC | OOS | 3146 | +0.01% | +0.04% | +0.14% | 0.65 |  |
| A favor dos top traders: posições compradas → compra | BTC | IS | 2380 | -0.01% | +0.01% | -0.14% | -0.40 |  |
| A favor dos top traders: posições compradas → compra | BTC | OOS | 3113 | +0.00% | -0.00% | +0.18% | 0.79 |  |
| Top traders compram enquanto varejo vende | BTC | IS | 3408 | +0.02% | +0.07% | +0.10% | 0.36 |  |
| Top traders compram enquanto varejo vende | BTC | OOS | 2337 | +0.01% | +0.04% | +0.23% | 0.95 |  |
| Contra o fluxo agressor extremo | BTC | IS | 339 | +0.02% | -0.02% | -0.30% | -0.36 |  |
| Contra o fluxo agressor extremo | BTC | OOS | 381 | -0.00% | -0.05% | +0.11% | 0.21 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | BTC | IS | 208 | +0.05% | +0.36% | +0.55% | 0.31 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | BTC | OOS | 170 | +0.02% | -0.01% | +0.37% | 0.36 |  |
| Contra o funding extremo | BTC | IS | 2900 | +0.04% | +0.13% | +0.72% | 2.03 |  |
| Contra o funding extremo | BTC | OOS | 2884 | +0.00% | +0.03% | +0.10% | 0.40 |  |
| Após candle 1m subida >5σ (próx. 5 min) | BTC | IS | 3429 |  |  |  | 0.74 | +0.010% |
| Após candle 1m subida >5σ (próx. 5 min) | BTC | OOS | 2230 |  |  |  | -0.38 | -0.003% |
| Após candle 1m queda <−5σ (próx. 5 min) | BTC | IS | 3241 |  |  |  | 2.95 | +0.054% |
| Após candle 1m queda <−5σ (próx. 5 min) | BTC | OOS | 2133 |  |  |  | 2.76 | +0.031% |
| Após candle 1m subida >5σ (próx. 15 min) | BTC | IS | 3429 |  |  |  | 1.95 | +0.034% |
| Após candle 1m subida >5σ (próx. 15 min) | BTC | OOS | 2230 |  |  |  | -0.85 | -0.011% |
| Após candle 1m queda <−5σ (próx. 15 min) | BTC | IS | 3241 |  |  |  | 3.00 | +0.065% |
| Após candle 1m queda <−5σ (próx. 15 min) | BTC | OOS | 2133 |  |  |  | 2.14 | +0.033% |
| Após candle 1m subida >5σ (próx. 60 min) | BTC | IS | 3429 |  |  |  | 2.97 | +0.072% |
| Após candle 1m subida >5σ (próx. 60 min) | BTC | OOS | 2230 |  |  |  | 0.02 | +0.000% |
| Após candle 1m queda <−5σ (próx. 60 min) | BTC | IS | 3241 |  |  |  | 4.40 | +0.122% |
| Após candle 1m queda <−5σ (próx. 60 min) | BTC | OOS | 2133 |  |  |  | 1.84 | +0.040% |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | ETH | IS | 2258 | +0.06% | +0.21% | +0.70% | 1.73 |  |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | ETH | OOS | 2565 | +0.02% | +0.06% | +0.21% | 0.62 |  |
| A favor dos top traders: posições compradas → compra | ETH | IS | 1247 | -0.02% | -0.11% | -0.69% | -1.39 |  |
| A favor dos top traders: posições compradas → compra | ETH | OOS | 3070 | -0.00% | +0.00% | -0.23% | -0.70 |  |
| Top traders compram enquanto varejo vende | ETH | IS | 2080 | +0.01% | +0.04% | -0.08% | -0.25 |  |
| Top traders compram enquanto varejo vende | ETH | OOS | 2718 | +0.01% | -0.00% | -0.24% | -0.78 |  |
| Contra o fluxo agressor extremo | ETH | IS | 222 | -0.01% | +0.04% | +0.09% | 0.08 |  |
| Contra o fluxo agressor extremo | ETH | OOS | 371 | +0.03% | -0.09% | +0.01% | 0.02 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | ETH | IS | 133 | +0.02% | +0.20% | -0.70% | -0.28 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | ETH | OOS | 154 | -0.02% | +0.06% | +0.48% | 0.28 |  |
| Contra o funding extremo | ETH | IS | 1404 | +0.02% | +0.11% | +0.52% | 0.89 |  |
| Contra o funding extremo | ETH | OOS | 2572 | -0.01% | +0.00% | +0.10% | 0.26 |  |
| Após candle 1m subida >5σ (próx. 5 min) | ETH | IS | 2883 |  |  |  | 1.18 | +0.023% |
| Após candle 1m subida >5σ (próx. 5 min) | ETH | OOS | 2386 |  |  |  | 1.77 | +0.021% |
| Após candle 1m queda <−5σ (próx. 5 min) | ETH | IS | 2981 |  |  |  | 3.35 | +0.104% |
| Após candle 1m queda <−5σ (próx. 5 min) | ETH | OOS | 2320 |  |  |  | 3.74 | +0.064% |
| Após candle 1m subida >5σ (próx. 15 min) | ETH | IS | 2883 |  |  |  | 2.36 | +0.058% |
| Após candle 1m subida >5σ (próx. 15 min) | ETH | OOS | 2386 |  |  |  | 1.15 | +0.021% |
| Após candle 1m queda <−5σ (próx. 15 min) | ETH | IS | 2981 |  |  |  | 5.30 | +0.180% |
| Após candle 1m queda <−5σ (próx. 15 min) | ETH | OOS | 2320 |  |  |  | 2.07 | +0.048% |
| Após candle 1m subida >5σ (próx. 60 min) | ETH | IS | 2883 |  |  |  | 5.34 | +0.171% |
| Após candle 1m subida >5σ (próx. 60 min) | ETH | OOS | 2386 |  |  |  | 2.20 | +0.062% |
| Após candle 1m queda <−5σ (próx. 60 min) | ETH | IS | 2981 |  |  |  | 6.16 | +0.282% |
| Após candle 1m queda <−5σ (próx. 60 min) | ETH | OOS | 2320 |  |  |  | 4.25 | +0.135% |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | SOL | IS | 2192 | +0.06% | +0.12% | +0.52% | 0.80 |  |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | SOL | OOS | 2800 | +0.02% | +0.06% | +0.39% | 1.03 |  |
| A favor dos top traders: posições compradas → compra | SOL | IS | 1482 | -0.01% | +0.01% | +0.32% | 0.40 |  |
| A favor dos top traders: posições compradas → compra | SOL | OOS | 3237 | +0.03% | +0.08% | +0.21% | 0.56 |  |
| Top traders compram enquanto varejo vende | SOL | IS | 1249 | +0.01% | +0.06% | +0.19% | 0.21 |  |
| Top traders compram enquanto varejo vende | SOL | OOS | 3933 | +0.03% | +0.11% | +0.29% | 0.90 |  |
| Contra o fluxo agressor extremo | SOL | IS | 286 | -0.01% | -0.14% | -0.30% | -0.22 |  |
| Contra o fluxo agressor extremo | SOL | OOS | 368 | +0.03% | +0.01% | +0.01% | 0.01 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | SOL | IS | 99 | +0.44% | +0.54% | +2.48% | 0.31 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | SOL | OOS | 125 | +0.42% | +0.71% | +1.20% | 0.45 |  |
| Contra o funding extremo | SOL | IS | 1597 | -0.03% | -0.10% | -0.70% | -0.55 |  |
| Contra o funding extremo | SOL | OOS | 2100 | -0.00% | -0.01% | -0.30% | -0.63 |  |
| Após candle 1m subida >5σ (próx. 5 min) | SOL | IS | 2210 |  |  |  | 0.93 | +0.026% |
| Após candle 1m subida >5σ (próx. 5 min) | SOL | OOS | 1709 |  |  |  | 2.40 | +0.048% |
| Após candle 1m queda <−5σ (próx. 5 min) | SOL | IS | 2096 |  |  |  | 3.87 | +0.132% |
| Após candle 1m queda <−5σ (próx. 5 min) | SOL | OOS | 1680 |  |  |  | 2.46 | +0.080% |
| Após candle 1m subida >5σ (próx. 15 min) | SOL | IS | 2210 |  |  |  | 2.72 | +0.112% |
| Após candle 1m subida >5σ (próx. 15 min) | SOL | OOS | 1709 |  |  |  | 3.42 | +0.106% |
| Após candle 1m queda <−5σ (próx. 15 min) | SOL | IS | 2096 |  |  |  | 6.74 | +0.297% |
| Após candle 1m queda <−5σ (próx. 15 min) | SOL | OOS | 1680 |  |  |  | 3.19 | +0.129% |
| Após candle 1m subida >5σ (próx. 60 min) | SOL | IS | 2210 |  |  |  | 5.85 | +0.355% |
| Após candle 1m subida >5σ (próx. 60 min) | SOL | OOS | 1709 |  |  |  | 3.53 | +0.160% |
| Após candle 1m queda <−5σ (próx. 60 min) | SOL | IS | 2096 |  |  |  | 9.71 | +0.680% |
| Após candle 1m queda <−5σ (próx. 60 min) | SOL | OOS | 1680 |  |  |  | 4.42 | +0.224% |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | DOGE | IS | 2094 | -0.03% | -0.05% | +0.04% | 0.07 |  |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | DOGE | OOS | 2505 | +0.04% | +0.04% | +0.24% | 0.53 |  |
| A favor dos top traders: posições compradas → compra | DOGE | IS | 1585 | +0.01% | +0.01% | +0.48% | 1.20 |  |
| A favor dos top traders: posições compradas → compra | DOGE | OOS | 3201 | +0.00% | +0.06% | +0.17% | 0.34 |  |
| Top traders compram enquanto varejo vende | DOGE | IS | 1574 | +0.01% | +0.04% | +0.56% | 1.30 |  |
| Top traders compram enquanto varejo vende | DOGE | OOS | 2596 | +0.03% | +0.10% | +0.37% | 0.83 |  |
| Contra o fluxo agressor extremo | DOGE | IS | 333 | +0.01% | +0.02% | +0.22% | 0.23 |  |
| Contra o fluxo agressor extremo | DOGE | OOS | 399 | -0.04% | +0.05% | +0.05% | 0.05 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | DOGE | IS | 121 | +0.25% | +0.23% | +1.96% | 0.60 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | DOGE | OOS | 143 | -0.20% | +0.04% | +1.52% | 0.43 |  |
| Contra o funding extremo | DOGE | IS | 1443 | +0.03% | +0.15% | +0.14% | 0.23 |  |
| Contra o funding extremo | DOGE | OOS | 2012 | -0.02% | -0.06% | -0.40% | -0.53 |  |
| Após candle 1m subida >5σ (próx. 5 min) | DOGE | IS | 3075 |  |  |  | 5.56 | +0.177% |
| Após candle 1m subida >5σ (próx. 5 min) | DOGE | OOS | 1936 |  |  |  | 2.11 | +0.059% |
| Após candle 1m queda <−5σ (próx. 5 min) | DOGE | IS | 3041 |  |  |  | 4.39 | +0.171% |
| Após candle 1m queda <−5σ (próx. 5 min) | DOGE | OOS | 1926 |  |  |  | 0.94 | +0.060% |
| Após candle 1m subida >5σ (próx. 15 min) | DOGE | IS | 3075 |  |  |  | 4.71 | +0.218% |
| Após candle 1m subida >5σ (próx. 15 min) | DOGE | OOS | 1936 |  |  |  | 1.82 | +0.073% |
| Após candle 1m queda <−5σ (próx. 15 min) | DOGE | IS | 3041 |  |  |  | 6.16 | +0.304% |
| Após candle 1m queda <−5σ (próx. 15 min) | DOGE | OOS | 1926 |  |  |  | 1.50 | +0.115% |
| Após candle 1m subida >5σ (próx. 60 min) | DOGE | IS | 3075 |  |  |  | 3.92 | +0.340% |
| Após candle 1m subida >5σ (próx. 60 min) | DOGE | OOS | 1936 |  |  |  | 2.20 | +0.124% |
| Após candle 1m queda <−5σ (próx. 60 min) | DOGE | IS | 3041 |  |  |  | 6.69 | +0.517% |
| Após candle 1m queda <−5σ (próx. 60 min) | DOGE | OOS | 1926 |  |  |  | 2.03 | +0.176% |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | XRP | IS | 1914 | +0.01% | +0.02% | +0.13% | 0.32 |  |
| Contra o varejo: contas muito compradas → vende (e vice-versa) | XRP | OOS | 2653 | +0.04% | +0.15% | +0.43% | 0.91 |  |
| A favor dos top traders: posições compradas → compra | XRP | IS | 1376 | +0.01% | +0.02% | +0.34% | 0.71 |  |
| A favor dos top traders: posições compradas → compra | XRP | OOS | 3139 | -0.00% | -0.04% | -0.26% | -0.61 |  |
| Top traders compram enquanto varejo vende | XRP | IS | 1857 | +0.03% | +0.08% | +0.39% | 0.96 |  |
| Top traders compram enquanto varejo vende | XRP | OOS | 3398 | +0.01% | +0.07% | +0.19% | 0.57 |  |
| Contra o fluxo agressor extremo | XRP | IS | 302 | -0.01% | -0.03% | +0.01% | 0.01 |  |
| Contra o fluxo agressor extremo | XRP | OOS | 405 | -0.02% | -0.08% | -0.28% | -0.30 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | XRP | IS | 130 | +0.36% | +0.16% | +0.69% | 0.25 |  |
| Cascata de liquidação: queda forte + OI despenca → compra | XRP | OOS | 134 | +0.06% | +0.49% | +1.74% | 0.53 |  |
| Contra o funding extremo | XRP | IS | 1195 | -0.01% | +0.04% | +0.35% | 0.52 |  |
| Contra o funding extremo | XRP | OOS | 2472 | +0.00% | +0.02% | -0.30% | -0.61 |  |
| Após candle 1m subida >5σ (próx. 5 min) | XRP | IS | 2812 |  |  |  | 5.49 | +0.150% |
| Após candle 1m subida >5σ (próx. 5 min) | XRP | OOS | 2318 |  |  |  | 2.71 | +0.060% |
| Após candle 1m queda <−5σ (próx. 5 min) | XRP | IS | 3107 |  |  |  | 4.41 | +0.149% |
| Após candle 1m queda <−5σ (próx. 5 min) | XRP | OOS | 2074 |  |  |  | 1.04 | +0.044% |
| Após candle 1m subida >5σ (próx. 15 min) | XRP | IS | 2812 |  |  |  | 4.79 | +0.190% |
| Após candle 1m subida >5σ (próx. 15 min) | XRP | OOS | 2318 |  |  |  | 2.63 | +0.100% |
| Após candle 1m queda <−5σ (próx. 15 min) | XRP | IS | 3107 |  |  |  | 4.87 | +0.205% |
| Após candle 1m queda <−5σ (próx. 15 min) | XRP | OOS | 2074 |  |  |  | 1.81 | +0.095% |
| Após candle 1m subida >5σ (próx. 60 min) | XRP | IS | 2812 |  |  |  | 3.38 | +0.186% |
| Após candle 1m subida >5σ (próx. 60 min) | XRP | OOS | 2318 |  |  |  | 5.20 | +0.252% |
| Após candle 1m queda <−5σ (próx. 60 min) | XRP | IS | 3107 |  |  |  | 7.55 | +0.417% |
| Após candle 1m queda <−5σ (próx. 60 min) | XRP | OOS | 2074 |  |  |  | 3.86 | +0.243% |


## L3. Sazonalidade por hora (UTC), média dos 5 ativos — retorno médio por minuto em centésimos de bp

Correlação do perfil horário IS × OOS: **-0.16** (perto de 0 = padrão não se repete). 4 melhores horas no IS: [5, 10, 21, 15]; retorno dessas horas no OOS: +0.018 vs média geral +0.008.

| hora_UTC | IS | OOS |
|---|---|---|
| 0 | +0.056 | -0.001 |
| 1 | +0.012 | -0.017 |
| 2 | -0.047 | +0.035 |
| 3 | -0.014 | +0.052 |
| 4 | +0.042 | +0.037 |
| 5 | +0.092 | -0.009 |
| 6 | +0.021 | -0.029 |
| 7 | +0.056 | +0.001 |
| 8 | -0.032 | +0.048 |
| 9 | -0.025 | +0.033 |
| 10 | +0.085 | -0.016 |
| 11 | +0.012 | +0.018 |
| 12 | +0.022 | -0.019 |
| 13 | +0.069 | -0.071 |
| 14 | -0.079 | +0.020 |
| 15 | +0.072 | +0.002 |
| 16 | +0.028 | +0.004 |
| 17 | +0.021 | +0.055 |
| 18 | +0.054 | -0.026 |
| 19 | +0.054 | -0.016 |
| 20 | +0.046 | -0.003 |
| 21 | +0.076 | +0.094 |
| 22 | +0.071 | +0.052 |
| 23 | -0.029 | -0.060 |

