# Resultados — A estrutura matemática do preço

## S1. Razão de variâncias por escala (1 = passeio aleatório; <1 reversão; >1 tendência)

Negrito = |z| > 3. Expoente de Hurst local ≈ 0,5 + ln(VR)/(2·ln q).

| ativo | período | 2m | 5m | 15m | 30m | 1h | 4h | 12h | 1d | 3d | 7d | 14d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | IS 2020–2023 | 0.99 | 0.95 | 0.90 | 0.88 | 0.84 | **0.81** | **0.77** | **0.81** | **0.79** | 0.84 | 0.86 |
| BTC | OOS 2024–2026 | 0.98 | 0.95 | 0.92 | 0.91 | 0.90 | **0.88** | **0.87** | **0.86** | 0.84 | 0.85 | 0.87 |
| ETH | IS 2020–2023 | 1.00 | 0.95 | 0.88 | 0.87 | 0.84 | **0.80** | **0.76** | **0.80** | **0.80** | 0.86 | 0.88 |
| ETH | OOS 2024–2026 | 0.97 | 0.95 | 0.92 | 0.92 | 0.91 | **0.91** | 0.94 | 0.94 | 0.95 | 0.96 | 1.00 |
| SOL | IS 2020–2023 | 1.00 | 0.97 | 0.94 | 0.92 | 0.90 | **0.86** | **0.83** | **0.85** | 0.83 | 0.87 | 0.99 |
| SOL | OOS 2024–2026 | 0.98 | 0.96 | 0.92 | 0.90 | 0.88 | **0.83** | **0.81** | **0.81** | **0.76** | 0.74 | 0.72 |
| DOGE | IS 2020–2023 | 1.01 | 0.98 | 0.92 | 0.90 | 0.88 | **0.80** | **0.81** | 0.98 | 0.90 | 0.99 | 1.04 |
| DOGE | OOS 2024–2026 | 1.01 | 1.01 | 0.95 | 0.91 | 0.86 | **0.80** | **0.78** | **0.79** | 0.82 | 0.84 | 0.88 |
| XRP | IS 2020–2023 | 0.99 | 0.96 | 0.92 | 0.90 | 0.86 | **0.79** | **0.75** | **0.78** | **0.75** | 0.79 | 0.84 |
| XRP | OOS 2024–2026 | 1.01 | 0.98 | 0.95 | 0.92 | 0.88 | **0.81** | **0.78** | **0.80** | **0.81** | 0.86 | 0.96 |


## S2. Ciclos de Fourier (retornos horários, períodos de 2h a 30 dias, limiar por 30 permutações)

| ativo | série | ciclos significativos (período em horas) | potência do maior pico / limiar 95% |
|---|---|---|---|
| BTC | retornos | nenhum | 0.86 |
| BTC | |retornos| (volatilidade) | 24.0h, 84.0h, 168.2h, 167.7h, 8.0h | 13.78 |
| ETH | retornos | nenhum | 0.95 |
| ETH | |retornos| (volatilidade) | 24.0h, 84.0h, 168.2h, 167.7h, 8.0h | 14.35 |
| SOL | retornos | nenhum | 0.94 |
| SOL | |retornos| (volatilidade) | 12.0h, 24.0h, 364.5h, 367.0h, 637.9h | 5.60 |
| DOGE | retornos | nenhum | 0.85 |
| DOGE | |retornos| (volatilidade) | 502.6h, 588.1h, 594.5h, 569.9h, 468.5h | 5.82 |
| XRP | retornos | nenhum | 0.77 |
| XRP | |retornos| (volatilidade) | 718.4h, 24.0h, 389.7h, 394.9h, 12.0h | 3.81 |


## S3. Memória da volatilidade vs memória do retorno

| ativo | autocorr |r| lag 1h | autocorr |r| lag 24h | autocorr |r| lag 168h | autocorr |r| lag 720h | autocorr r lag 1h |
|---|---|---|---|---|---|
| BTC | 0.30 | 0.17 | 0.14 | 0.08 | -0.017 |
| ETH | 0.28 | 0.18 | 0.15 | 0.08 | -0.006 |
| SOL | 0.33 | 0.23 | 0.14 | 0.09 | -0.019 |
| DOGE | 0.41 | 0.26 | 0.12 | 0.07 | -0.022 |
| XRP | 0.36 | 0.21 | 0.13 | 0.08 | -0.028 |

