# Resultados — Contraparte do day trader: reversão com ordens limitadas (maker)

Bollinger(20, 2) em 5 min, carteira igual BTC/ETH/SOL/DOGE/XRP (perpétuos). Entrada e alvo com ordem limitada; stop de 4 desvios e stop de tempo de 1h a mercado (taxa taker + slippage). Funding não incluído (posições < 1h na média).

| estratégia | período | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês |
|---|---|---|---|---|---|---|---|---|
| maker 0,02% (VIP0) · atravessar 1bp | total | -99.9% | -13.49 | -100.0% | -42.6% | -41.6% | 0% | -72.9% |
| maker 0,02% (VIP0) · atravessar 1bp | IS 2020–2023 | -99.9% | -13.07 | -100.0% | -43.8% | -41.8% | 0% | -72.9% |
| maker 0,02% (VIP0) · atravessar 1bp | OOS 2024–2026 | -99.8% | -14.39 | -100.0% | -40.8% | -41.2% | 0% | -55.6% |
| maker 0,02% · atravessar 3bp (fila pior) | total | -100.0% | -17.03 | -100.0% | -49.7% | -49.5% | 0% | -76.3% |
| maker 0,02% · atravessar 3bp (fila pior) | IS 2020–2023 | -100.0% | -16.48 | -100.0% | -51.1% | -50.1% | 0% | -76.3% |
| maker 0,02% · atravessar 3bp (fila pior) | OOS 2024–2026 | -100.0% | -18.26 | -100.0% | -47.9% | -48.7% | 0% | -60.0% |
| maker 0% (VIP alto/programa MM) · 1bp | total | -98.7% | -8.33 | -100.0% | -29.3% | -27.8% | 0% | -66.3% |
| maker 0% (VIP alto/programa MM) · 1bp | IS 2020–2023 | -99.0% | -8.23 | -100.0% | -30.6% | -27.9% | 0% | -66.3% |
| maker 0% (VIP alto/programa MM) · 1bp | OOS 2024–2026 | -98.0% | -8.62 | -100.0% | -27.5% | -27.7% | 0% | -45.3% |
| maker 0,02% · sem exigir atravessar (otimista) | total | -99.7% | -11.44 | -100.0% | -37.8% | -36.7% | 0% | -70.2% |
| maker 0,02% · sem exigir atravessar (otimista) | IS 2020–2023 | -99.8% | -11.15 | -100.0% | -39.1% | -37.0% | 0% | -70.2% |
| maker 0,02% · sem exigir atravessar (otimista) | OOS 2024–2026 | -99.6% | -12.11 | -100.0% | -36.0% | -36.3% | 0% | -51.7% |


### Operações por dia

| cenário | ativo | trades/dia |
|---|---|---|
| maker 0,02% (VIP0) · atravessar 1bp | BTC | 20.20 |
| maker 0,02% · atravessar 3bp (fila pior) | BTC | 18.10 |
| maker 0% (VIP alto/programa MM) · 1bp | BTC | 20.20 |
| maker 0,02% · sem exigir atravessar (otimista) | BTC | 21.50 |
| maker 0,02% (VIP0) · atravessar 1bp | ETH | 20.80 |
| maker 0,02% · atravessar 3bp (fila pior) | ETH | 19.10 |
| maker 0% (VIP alto/programa MM) · 1bp | ETH | 20.80 |
| maker 0,02% · sem exigir atravessar (otimista) | ETH | 21.80 |
| maker 0,02% (VIP0) · atravessar 1bp | SOL | 20.50 |
| maker 0,02% · atravessar 3bp (fila pior) | SOL | 19.30 |
| maker 0% (VIP alto/programa MM) · 1bp | SOL | 20.50 |
| maker 0,02% · sem exigir atravessar (otimista) | SOL | 21.20 |
| maker 0,02% (VIP0) · atravessar 1bp | DOGE | 20.90 |
| maker 0,02% · atravessar 3bp (fila pior) | DOGE | 19.40 |
| maker 0% (VIP alto/programa MM) · 1bp | DOGE | 20.90 |
| maker 0,02% · sem exigir atravessar (otimista) | DOGE | 21.70 |
| maker 0,02% (VIP0) · atravessar 1bp | XRP | 20.60 |
| maker 0,02% · atravessar 3bp (fila pior) | XRP | 19.00 |
| maker 0% (VIP alto/programa MM) · 1bp | XRP | 20.60 |
| maker 0,02% · sem exigir atravessar (otimista) | XRP | 21.50 |

