# Resultados — Cripto

Total aproximado de variantes testadas: **190** (usado no Sharpe deflacionado).

Gerado por `research/strategies/cripto.py`. Dados diários (UTC). Caixa = USDT a 0% (conservador). Custos: spot 0.15%/lado, perpétuo 0.08%/lado + funding real. In-sample até 2022, out-of-sample 2023–2026.

Universo: **656 pares USDT** (inclui deslistados), 2017-08-17 → 2026-10-31; funding de **465 perpétuos**.

## E. Referências (buy & hold)

| estratégia | período | CAGR | vol | sharpe | maxDD | calmar | DSR |
|---|---|---|---|---|---|---|---|
| Buy & hold BTC | 2018–2026 | 21.7% | 64.0% | 0.63 | -81.2% | 0.27 | 0.17 |
| Buy & hold BTC | IS 2018–2022 | 3.8% | 74.9% | 0.43 | -81.2% | 0.05 | 0.03 |
| Buy & hold BTC | OOS 2023–2026 | 49.6% | 46.1% | 1.10 | -53.0% | 0.94 | 0.25 |
| Buy & hold ETH | 2018–2026 | 13.5% | 84.3% | 0.58 | -94.0% | 0.14 | 0.13 |
| Buy & hold ETH | IS 2018–2022 | 10.3% | 97.7% | 0.60 | -94.0% | 0.11 | 0.07 |
| Buy & hold ETH | OOS 2023–2026 | 18.0% | 62.6% | 0.57 | -67.6% | 0.27 | 0.04 |
| Top-10 por volume, pesos iguais (mensal) | 2018–2026 | -12.4% | 81.0% | 0.25 | -92.5% | -0.13 | 0.02 |
| Top-10 por volume, pesos iguais (mensal) | IS 2018–2022 | -25.4% | 92.0% | 0.16 | -91.4% | -0.28 | 0.01 |
| Top-10 por volume, pesos iguais (mensal) | OOS 2023–2026 | 7.8% | 64.0% | 0.44 | -71.6% | 0.11 | 0.02 |


## F. Tendência — grade de parâmetros (escolhe a melhor regra no IS, mede no OOS)

BTC longo: IS 2012–2019, OOS 2020–2026. Binance: IS 2018–2022, OOS 2023–2026. Sharpe OOS do buy & hold: BTC 1.10, ETH 0.57.

| ativo | modo | regras | mediana_sh_IS | mediana_sh_OOS | %_OOS>0 | melhor_IS | sh_IS | → sh_OOS | CAGR_OOS | maxDD_OOS |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC 2012–2026 (Bitstamp) | long/caixa | 23 | 1.63 | 0.90 | 100% | Donchian 20/10 | 1.94 | 0.83 | 0.27 | -0.57 |
| BTC 2012–2026 (Bitstamp) | long/short | 23 | 1.28 | 0.37 | 96% | TSMOM 60d | 1.50 | 0.62 | 0.21 | -0.59 |
| BTC (Binance) | long/caixa | 23 | 1.01 | 0.99 | 100% | Donchian 100/50 | 1.33 | 0.44 | 0.09 | -0.37 |
| BTC (Binance) | long/short | 23 | 0.77 | 0.42 | 87% | Donchian 100/50 | 1.03 | -0.46 | -0.27 | -0.71 |
| ETH (Binance, desde 2018-08-17) | long/caixa | 23 | 1.01 | 0.64 | 91% | Donchian 20/10 | 1.35 | 0.29 | 0.04 | -0.51 |
| ETH (Binance, desde 2018-08-17) | long/short | 23 | 0.66 | 0.37 | 78% | TSMOM 30d | 0.97 | 0.80 | 0.36 | -0.50 |


### F2. Robustez: Sharpe médio de cada regra (long/caixa) nos 3 testes — top 10 e piores 5

| regra | sh_IS | sh_OOS |
|---|---|---|
| preço>MM50 | 1.23 | 1.25 |
| TSMOM 30d | 1.21 | 1.07 |
| MM5>MM50 | 1.27 | 1.06 |
| TSMOM 60d | 1.28 | 1.06 |
| TSMOM 14d | 1.25 | 0.96 |
| preço>MM150 | 1.24 | 0.96 |
| MM10>MM50 | 1.26 | 0.95 |
| preço>MM100 | 1.24 | 0.93 |
| Donchian 50/25 | 1.16 | 0.92 |
| TSMOM 365d | 1.02 | 0.87 |


| regra | sh_IS | sh_OOS |
|---|---|---|
| TSMOM 180d | 1.08 | 0.60 |
| MM20>MM200 | 1.12 | 0.60 |
| MM50>MM200 | 1.12 | 0.49 |
| TSMOM 7d | 1.15 | 0.44 |
| preço>MM10 | 1.01 | 0.38 |


### F3. Tendência em cesta diversificada (top-20 por volume)

| estratégia | período | CAGR | vol | sharpe | maxDD | calmar | exposicao | DSR |
|---|---|---|---|---|---|---|---|---|
| Cesta top-20, cada moeda > MM20 (long/caixa) | 2018–2026 | 12.3% | 43.4% | 0.48 | -72.6% | 0.17 | 43.6% | 0.08 |
| Cesta top-20, cada moeda > MM20 (long/caixa) | IS 2018–2022 | 28.1% | 46.0% | 0.77 | -57.8% | 0.49 | 41.2% | 0.13 |
| Cesta top-20, cada moeda > MM20 (long/caixa) | OOS 2023–2026 | -5.5% | 39.8% | 0.06 | -68.4% | -0.08 | 46.6% | 0.00 |
| Cesta top-20, cada moeda > MM50 (long/caixa) | 2018–2026 | 13.6% | 47.8% | 0.51 | -75.9% | 0.18 | 46.9% | 0.09 |
| Cesta top-20, cada moeda > MM50 (long/caixa) | IS 2018–2022 | 32.2% | 50.3% | 0.81 | -61.4% | 0.52 | 42.6% | 0.15 |
| Cesta top-20, cada moeda > MM50 (long/caixa) | OOS 2023–2026 | -6.7% | 44.4% | 0.06 | -65.6% | -0.10 | 52.5% | 0.00 |
| Cesta top-20, cada moeda > MM100 (long/caixa) | 2018–2026 | 2.9% | 51.5% | 0.32 | -83.3% | 0.04 | 48.5% | 0.03 |
| Cesta top-20, cada moeda > MM100 (long/caixa) | IS 2018–2022 | 14.2% | 53.7% | 0.52 | -71.5% | 0.20 | 42.4% | 0.05 |
| Cesta top-20, cada moeda > MM100 (long/caixa) | OOS 2023–2026 | -10.1% | 48.5% | 0.02 | -67.1% | -0.15 | 56.4% | 0.00 |


## G. Reversão à média (BTC/ETH, diário)

| estratégia | período | CAGR | vol | sharpe | maxDD | calmar | exposicao | DSR |
|---|---|---|---|---|---|---|---|---|
| BTC: RSI(2)<10, sai > MM5 | 2018–2026 | -1.0% | 36.8% | 0.17 | -61.0% | -0.02 | 20.7% | 0.01 |
| BTC: RSI(2)<10, sai > MM5 | IS 2018–2022 | -8.6% | 44.0% | 0.03 | -61.0% | -0.14 | 21.2% | 0.00 |
| BTC: RSI(2)<10, sai > MM5 | OOS 2023–2026 | 9.9% | 24.3% | 0.51 | -34.3% | 0.29 | 19.9% | 0.03 |
| BTC: RSI(2)<10 acima MM200 | 2018–2026 | 4.5% | 20.1% | 0.32 | -34.3% | 0.13 | 8.6% | 0.03 |
| BTC: RSI(2)<10 acima MM200 | IS 2018–2022 | 0.0% | 21.8% | 0.11 | -33.4% | 0.00 | 6.2% | 0.00 |
| BTC: RSI(2)<10 acima MM200 | OOS 2023–2026 | 10.6% | 17.6% | 0.66 | -23.4% | 0.45 | 11.6% | 0.06 |
| BTC: Bollinger(20,2) inferior → média | 2018–2026 | -5.7% | 38.6% | 0.05 | -71.4% | -0.08 | 23.6% | 0.00 |
| BTC: Bollinger(20,2) inferior → média | IS 2018–2022 | -18.3% | 46.9% | -0.18 | -71.4% | -0.26 | 26.8% | 0.00 |
| BTC: Bollinger(20,2) inferior → média | OOS 2023–2026 | 13.6% | 23.9% | 0.65 | -38.5% | 0.35 | 19.3% | 0.06 |
| BTC: Compra após 3 quedas | 2018–2026 | 4.3% | 21.5% | 0.31 | -57.9% | 0.08 | 10.2% | 0.03 |
| BTC: Compra após 3 quedas | IS 2018–2022 | -0.4% | 24.6% | 0.11 | -56.9% | -0.01 | 9.4% | 0.00 |
| BTC: Compra após 3 quedas | OOS 2023–2026 | 10.8% | 16.6% | 0.70 | -13.5% | 0.80 | 11.2% | 0.07 |
| BTC: Short RSI(2)>90 (perp) | 2018–2026 | -26.9% | 31.7% | -0.83 | -95.6% | -0.28 | 24.7% | 0.00 |
| BTC: Short RSI(2)>90 (perp) | IS 2018–2022 | -29.7% | 36.4% | -0.78 | -92.2% | -0.32 | 24.8% | 0.00 |
| BTC: Short RSI(2)>90 (perp) | OOS 2023–2026 | -23.2% | 24.3% | -0.96 | -66.8% | -0.35 | 24.6% | 0.00 |
| ETH: RSI(2)<10, sai > MM5 | 2018–2026 | -10.1% | 46.5% | 0.01 | -78.7% | -0.13 | 20.2% | 0.00 |
| ETH: RSI(2)<10, sai > MM5 | IS 2018–2022 | -19.5% | 54.7% | -0.12 | -78.4% | -0.25 | 21.4% | 0.00 |
| ETH: RSI(2)<10, sai > MM5 | OOS 2023–2026 | 3.9% | 32.9% | 0.28 | -38.4% | 0.10 | 18.7% | 0.01 |
| ETH: RSI(2)<10 acima MM200 | 2018–2026 | 2.9% | 27.2% | 0.24 | -39.9% | 0.07 | 7.8% | 0.02 |
| ETH: RSI(2)<10 acima MM200 | IS 2018–2022 | 1.4% | 31.7% | 0.21 | -37.9% | 0.04 | 6.9% | 0.01 |
| ETH: RSI(2)<10 acima MM200 | OOS 2023–2026 | 4.8% | 20.0% | 0.33 | -23.5% | 0.20 | 8.9% | 0.01 |
| ETH: Bollinger(20,2) inferior → média | 2018–2026 | -12.4% | 47.3% | -0.04 | -81.4% | -0.15 | 28.0% | 0.00 |
| ETH: Bollinger(20,2) inferior → média | IS 2018–2022 | -15.9% | 54.7% | -0.04 | -81.4% | -0.20 | 30.0% | 0.00 |
| ETH: Bollinger(20,2) inferior → média | OOS 2023–2026 | -7.7% | 35.5% | -0.05 | -58.7% | -0.13 | 25.4% | 0.00 |
| ETH: Compra após 3 quedas | 2018–2026 | 4.0% | 32.0% | 0.28 | -63.3% | 0.06 | 9.7% | 0.02 |
| ETH: Compra após 3 quedas | IS 2018–2022 | 7.0% | 37.3% | 0.37 | -63.3% | 0.11 | 9.3% | 0.02 |
| ETH: Compra após 3 quedas | OOS 2023–2026 | 0.1% | 23.2% | 0.12 | -31.6% | 0.00 | 10.2% | 0.00 |
| ETH: Short RSI(2)>90 (perp) | 2018–2026 | -35.3% | 40.0% | -0.88 | -98.0% | -0.36 | 22.7% | 0.00 |
| ETH: Short RSI(2)>90 (perp) | IS 2018–2022 | -37.5% | 47.2% | -0.75 | -91.4% | -0.41 | 23.5% | 0.00 |
| ETH: Short RSI(2)>90 (perp) | OOS 2023–2026 | -32.4% | 28.0% | -1.25 | -79.1% | -0.41 | 21.6% | 0.00 |


## H. Cross-section (ranking entre moedas, quintis, rebalanceamento semanal)

Vendido só em moedas com perpétuo listado na data; vendido recebe/paga funding real.

| sinal | lookback | universo | modo | sh_IS | sh_OOS | CAGR_OOS | maxDD_OOS |
|---|---|---|---|---|---|---|---|
| momentum | 7 | 20 | long/short | 0.30 | -0.23 | -0.15 | -0.71 |
| momentum | 7 | 20 | long-only | 0.41 | -0.16 | -0.41 | -0.95 |
| momentum | 7 | 50 | long/short | -0.18 | -0.14 | -0.08 | -0.41 |
| momentum | 7 | 50 | long-only | 0.18 | -0.15 | -0.38 | -0.96 |
| momentum | 14 | 20 | long/short | 0.48 | 0.32 | 0.05 | -0.47 |
| momentum | 14 | 20 | long-only | 0.61 | 0.02 | -0.32 | -0.91 |
| momentum | 14 | 50 | long/short | 0.53 | 0.27 | 0.04 | -0.50 |
| momentum | 14 | 50 | long-only | 0.78 | -0.03 | -0.32 | -0.95 |
| momentum | 30 | 20 | long/short | 0.40 | -0.37 | -0.20 | -0.74 |
| momentum | 30 | 20 | long-only | 0.37 | -0.37 | -0.55 | -0.98 |
| momentum | 30 | 50 | long/short | 0.44 | -0.64 | -0.21 | -0.68 |
| momentum | 30 | 50 | long-only | 0.60 | -0.50 | -0.55 | -0.98 |
| momentum | 60 | 20 | long/short | 0.05 | -0.46 | -0.22 | -0.69 |
| momentum | 60 | 20 | long-only | 0.11 | -0.44 | -0.59 | -0.99 |
| momentum | 60 | 50 | long/short | 0.12 | -0.94 | -0.28 | -0.71 |
| momentum | 60 | 50 | long-only | 0.42 | -0.55 | -0.58 | -0.98 |
| momentum | 90 | 20 | long/short | 0.18 | -0.67 | -0.28 | -0.73 |
| momentum | 90 | 20 | long-only | 0.19 | -0.40 | -0.57 | -0.98 |
| momentum | 90 | 50 | long/short | 0.29 | -1.15 | -0.32 | -0.79 |
| momentum | 90 | 50 | long-only | 0.48 | -0.63 | -0.59 | -0.99 |
| reversão | 1 | 20 | long/short | -1.41 | -2.34 | -0.63 | -0.98 |
| reversão | 1 | 50 | long/short | -1.48 | -2.32 | -0.52 | -0.95 |
| reversão | 3 | 20 | long/short | -0.96 | -0.61 | -0.27 | -0.80 |
| reversão | 3 | 50 | long/short | -0.60 | -0.86 | -0.27 | -0.73 |
| reversão | 7 | 20 | long/short | -1.19 | -0.52 | -0.24 | -0.75 |
| reversão | 7 | 50 | long/short | -0.97 | -0.94 | -0.27 | -0.76 |


### H2. Momentum long-only concentrado (top-5 de 50) com/sem filtro de tendência do BTC

| estratégia | período | CAGR | vol | sharpe | maxDD | calmar | exposicao | DSR |
|---|---|---|---|---|---|---|---|---|
| Top-5 momentum 30d | 2018–2026 | -46.4% | 107.1% | -0.04 | -100.0% | -0.46 | 91.6% | 0.00 |
| Top-5 momentum 30d | IS 2018–2022 | 2.2% | 107.9% | 0.57 | -96.0% | 0.02 | 85.2% | 0.06 |
| Top-5 momentum 30d | OOS 2023–2026 | -76.9% | 105.8% | -0.86 | -99.9% | -0.77 | 100.0% | 0.00 |
| Top-5 momentum 30d + filtro BTC>MM50 | 2018–2026 | 5.1% | 79.0% | 0.45 | -96.9% | 0.05 | 49.5% | 0.07 |
| Top-5 momentum 30d + filtro BTC>MM50 | IS 2018–2022 | 80.8% | 75.6% | 1.15 | -69.8% | 1.16 | 41.4% | 0.39 |
| Top-5 momentum 30d + filtro BTC>MM50 | OOS 2023–2026 | -48.3% | 83.1% | -0.38 | -96.5% | -0.50 | 60.0% | 0.00 |
| Top-5 momentum 60d + filtro BTC>MM50 | 2018–2026 | -13.3% | 75.3% | 0.18 | -99.3% | -0.13 | 49.5% | 0.01 |
| Top-5 momentum 60d + filtro BTC>MM50 | IS 2018–2022 | 70.4% | 72.0% | 1.09 | -69.5% | 1.01 | 41.4% | 0.35 |
| Top-5 momentum 60d + filtro BTC>MM50 | OOS 2023–2026 | -64.1% | 79.2% | -0.90 | -99.2% | -0.65 | 60.0% | 0.00 |
| Top-5 momentum 90d + filtro BTC>MM100 | 2018–2026 | -12.5% | 75.2% | 0.20 | -96.4% | -0.13 | 50.8% | 0.01 |
| Top-5 momentum 90d + filtro BTC>MM100 | IS 2018–2022 | 28.2% | 72.9% | 0.71 | -77.9% | 0.36 | 42.6% | 0.11 |
| Top-5 momentum 90d + filtro BTC>MM100 | OOS 2023–2026 | -46.9% | 78.0% | -0.42 | -95.8% | -0.49 | 61.6% | 0.00 |


## I. Carry de funding (compra spot + vende perpétuo, delta-neutro)

### I1. Funding anual acumulado (o que o vendido do perpétuo recebe)

| ativo | ano | funding_anual | %dias_negativos |
|---|---|---|---|
| BTC | 2020 | 17.2% | 14% |
| BTC | 2021 | 30.6% | 8% |
| BTC | 2022 | 4.2% | 20% |
| BTC | 2023 | 7.9% | 8% |
| BTC | 2024 | 12.0% | 7% |
| BTC | 2025 | 5.1% | 8% |
| BTC | 2026 | 2.6% | 23% |
| ETH | 2020 | 27.5% | 1% |
| ETH | 2021 | 37.5% | 3% |
| ETH | 2022 | 0.8% | 33% |
| ETH | 2023 | 8.3% | 6% |
| ETH | 2024 | 13.0% | 3% |
| ETH | 2025 | 4.9% | 10% |
| ETH | 2026 | 1.7% | 29% |


### I2. Retorno sobre o capital (capital = 1,5× notional; custos nas duas pernas; BTC/ETH incluem a oscilação diária spot×perpétuo; Top-5 só funding)

| estratégia | período | CAGR | vol | sharpe | maxDD | calmar | exposicao | DSR |
|---|---|---|---|---|---|---|---|---|
| Carry BTC sempre | 2018–2026 | 7.9% | 0.9% | 8.54 | -1.6% | 5.10 | 100.0% | 1.00 |
| Carry BTC sempre | IS 2018–2022 | 12.0% | 1.3% | 9.01 | -1.6% | 7.68 | 99.9% | 1.00 |
| Carry BTC sempre | OOS 2023–2026 | 4.9% | 0.4% | 12.62 | -0.3% | 17.23 | 100.0% | 1.00 |
| Carry ETH sempre | 2018–2026 | 9.3% | 1.2% | 7.50 | -1.2% | 7.81 | 100.0% | 1.00 |
| Carry ETH sempre | IS 2018–2022 | 15.2% | 1.7% | 8.36 | -1.2% | 12.74 | 99.9% | 1.00 |
| Carry ETH sempre | OOS 2023–2026 | 4.9% | 0.4% | 11.72 | -0.4% | 11.60 | 100.0% | 1.00 |
| Carry BTC+ETH, só se funding 7d > 0 | 2018–2026 | 7.5% | 1.0% | 6.96 | -1.5% | 5.12 | 90.0% | 1.00 |
| Carry BTC+ETH, só se funding 7d > 0 | IS 2018–2022 | 12.2% | 1.4% | 7.99 | -1.2% | 9.97 | 88.0% | 1.00 |
| Carry BTC+ETH, só se funding 7d > 0 | OOS 2023–2026 | 3.9% | 0.5% | 8.19 | -1.5% | 2.69 | 91.6% | 1.00 |
| Carry Top-5 funding 7d (entre top-30 vol.) | 2018–2026 | 1.7% | 2.5% | 0.68 | -25.4% | 0.07 | 98.8% | 0.18 |
| Carry Top-5 funding 7d (entre top-30 vol.) | IS 2018–2022 | 12.2% | 2.3% | 5.06 | -6.3% | 1.94 | 97.3% | 1.00 |
| Carry Top-5 funding 7d (entre top-30 vol.) | OOS 2023–2026 | -5.8% | 2.7% | -2.22 | -20.5% | -0.28 | 100.0% | 0.00 |


Risco não capturado no backtest: falência/bloqueio da corretora (ex.: FTX 2022), liquidação do vendido em alta brusca se a margem for curta, descolamento temporário entre spot e perpétuo.

## J. Sazonalidade e padrões gráficos

### J1. BTC — retorno médio por dia da semana (2018–2026)

| dia | media_diaria | t |
|---|---|---|
| seg | 0.336% | 1.85 |
| ter | -0.025% | -0.16 |
| qua | 0.342% | 2.08 |
| qui | -0.300% | -1.62 |
| sex | 0.250% | 1.56 |
| sáb | 0.139% | 1.39 |
| dom | 0.033% | 0.26 |


### J2. Padrões de candle — retorno 5 dias após o sinal vs média do universo (top-50)

| padrão | período | eventos | ret_5d_médio | excesso_vs_média | t | excesso_líq_custos |
|---|---|---|---|---|---|---|
| Engolfo de alta | IS 2018–2022 | 5105 | 0.96% | 0.36% | 1.54 | 0.06% |
| Engolfo de alta | OOS 2023–2026 | 5711 | -0.49% | -0.41% | -2.36 | -0.71% |
| Martelo | IS 2018–2022 | 1783 | -0.03% | -0.64% | -1.88 | -0.94% |
| Martelo | OOS 2023–2026 | 1761 | -0.19% | -0.11% | -0.38 | -0.41% |
| Doji após queda | IS 2018–2022 | 2151 | -0.16% | -0.77% | -2.16 | -1.07% |
| Doji após queda | OOS 2023–2026 | 2189 | -0.37% | -0.29% | -1.11 | -0.59% |
| Três soldados | IS 2018–2022 | 6673 | 1.48% | 0.87% | 3.83 | 0.57% |
| Três soldados | OOS 2023–2026 | 6994 | 0.15% | 0.23% | 1.30 | -0.07% |
| Rompimento máx. 20d | IS 2018–2022 | 7017 | 2.76% | 2.16% | 8.26 | 1.86% |
| Rompimento máx. 20d | OOS 2023–2026 | 6923 | 1.04% | 1.12% | 5.52 | 0.82% |

