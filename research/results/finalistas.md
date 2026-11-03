# Finalistas — análise detalhada

Gerado por `research/strategies/finalistas.py`.

## 1. Tendência em BTC/ETH — média de 23 regras (long/caixa)

Posição diária = fração das 23 regras de tendência que estão compradas (0 a 100%). Nenhum parâmetro foi escolhido olhando o resultado: todas as regras da grade entram com o mesmo peso.

### 1a. BTC desde 2012 (Bitstamp)

| estratégia | período | CAGR | vol | sharpe | maxDD | calmar |
|---|---|---|---|---|---|---|
| BTC buy & hold | 2012-08–2026 | 83.7% | 76.0% | 1.19 | -84.9% | 0.99 |
| BTC buy & hold | 2012-08–2019 | 134.3% | 88.3% | 1.41 | -84.9% | 1.58 |
| BTC buy & hold | 2020–2026 | 41.4% | 60.1% | 0.88 | -76.7% | 0.54 |
| BTC tendência | 2012-08–2026 | 90.0% | 53.7% | 1.47 | -68.6% | 1.31 |
| BTC tendência | 2012-08–2019 | 156.6% | 65.6% | 1.77 | -68.6% | 2.28 |
| BTC tendência | 2020–2026 | 37.4% | 36.6% | 1.05 | -46.5% | 0.80 |
| BTC tendência + vol-alvo 50% | 2012-08–2026 | 65.5% | 34.0% | 1.65 | -42.8% | 1.53 |
| BTC tendência + vol-alvo 50% | 2012-08–2019 | 108.3% | 37.0% | 2.17 | -37.0% | 2.92 |
| BTC tendência + vol-alvo 50% | 2020–2026 | 29.2% | 30.3% | 0.99 | -42.8% | 0.68 |
| BTC tendência (custo 2×) | 2012-08–2026 | 85.7% | 53.7% | 1.43 | -68.6% | 1.25 |
| BTC tendência (custo 2×) | 2012-08–2019 | 151.4% | 65.6% | 1.74 | -68.6% | 2.21 |
| BTC tendência (custo 2×) | 2020–2026 | 33.9% | 36.6% | 0.98 | -48.8% | 0.70 |


### 1b. Binance (BTC desde 2018; ETH e 50/50 desde 2018-08-17, após o aquecimento das regras)

| estratégia | período | CAGR | vol | sharpe | maxDD | calmar |
|---|---|---|---|---|---|---|
| BTC buy & hold | início–2026 | 21.7% | 64.0% | 0.63 | -81.2% | 0.27 |
| BTC buy & hold | início–2022 | 3.8% | 74.9% | 0.43 | -81.2% | 0.05 |
| BTC buy & hold | 2023–2026 | 49.6% | 46.1% | 1.10 | -53.0% | 0.94 |
| BTC tendência | início–2026 | 36.0% | 36.2% | 1.03 | -46.5% | 0.77 |
| BTC tendência | início–2022 | 39.0% | 40.3% | 1.02 | -46.4% | 0.84 |
| BTC tendência | 2023–2026 | 32.1% | 30.2% | 1.07 | -27.0% | 1.19 |
| ETH buy & hold | início–2026 | 28.5% | 82.0% | 0.72 | -79.3% | 0.36 |
| ETH buy & hold | início–2022 | 38.5% | 95.9% | 0.83 | -79.3% | 0.49 |
| ETH buy & hold | 2023–2026 | 18.0% | 62.6% | 0.57 | -67.6% | 0.27 |
| ETH tendência | início–2026 | 43.5% | 50.2% | 0.97 | -47.3% | 0.92 |
| ETH tendência | início–2022 | 67.0% | 59.6% | 1.16 | -47.3% | 1.42 |
| ETH tendência | 2023–2026 | 20.6% | 36.5% | 0.69 | -37.8% | 0.55 |
| 50/50 BTC+ETH buy & hold | início–2026 | 35.7% | 68.5% | 0.79 | -76.3% | 0.47 |
| 50/50 BTC+ETH buy & hold | início–2022 | 36.3% | 80.3% | 0.80 | -76.3% | 0.48 |
| 50/50 BTC+ETH buy & hold | 2023–2026 | 35.0% | 51.9% | 0.84 | -59.9% | 0.58 |
| 50/50 BTC+ETH tendência | início–2026 | 43.6% | 40.5% | 1.10 | -44.5% | 0.98 |
| 50/50 BTC+ETH tendência | início–2022 | 59.6% | 47.3% | 1.23 | -44.5% | 1.34 |
| 50/50 BTC+ETH tendência | 2023–2026 | 27.2% | 30.9% | 0.93 | -29.8% | 0.91 |


### 1c. Ano a ano (Binance)

| ano | BTC buy & hold | BTC tendência | ETH buy & hold | ETH tendência | 50/50 BTC+ETH buy & hold | 50/50 BTC+ETH tendência |
|---|---|---|---|---|---|---|
| 2018 | -73% | -9% | -54% | -9% | -47% | -9% |
| 2019 | 94% | 85% | -2% | 23% | 42% | 53% |
| 2020 | 302% | 184% | 470% | 201% | 395% | 201% |
| 2021 | 60% | 55% | 399% | 274% | 199% | 154% |
| 2022 | -64% | -30% | -67% | -25% | -65% | -27% |
| 2023 | 156% | 77% | 91% | 32% | 123% | 54% |
| 2024 | 121% | 73% | 46% | 28% | 83% | 50% |
| 2025 | -6% | -5% | -11% | 17% | -6% | 7% |
| 2026 | -11% | 0% | -24% | 4% | -17% | 2% |


## 2. Carry de funding e "tendência + carry no caixa"

Carry puro: compra spot + vende perpétuo na mesma quantidade (exposição zero ao preço) e recebe o funding. Tendência + carry: mantém 100% do capital em spot e vende perpétuo na fração `1 − sinal de tendência`; assim, quando a tendência manda sair, a posição fica neutra e passa a receber funding em vez de ficar parada. Exige conta com margem unificada (spot como garantia). Inclui custos e a oscilação diária spot×perpétuo.

| estratégia | período | CAGR | vol | sharpe | maxDD | calmar |
|---|---|---|---|---|---|---|
| BTC buy & hold | 2020–2026 | 41.6% | 59.9% | 0.89 | -76.6% | 0.54 |
| BTC buy & hold | 2020–2022 | 31.9% | 73.9% | 0.76 | -76.6% | 0.42 |
| BTC buy & hold | 2023–2026 | 49.6% | 46.1% | 1.10 | -53.0% | 0.94 |
| BTC tendência (caixa 0%) | 2020–2026 | 37.9% | 36.4% | 1.06 | -46.5% | 0.82 |
| BTC tendência (caixa 0%) | 2020–2022 | 45.7% | 43.1% | 1.09 | -46.4% | 0.98 |
| BTC tendência (caixa 0%) | 2023–2026 | 32.1% | 30.2% | 1.07 | -27.0% | 1.19 |
| BTC tendência + carry no caixa | 2020–2026 | 42.5% | 36.4% | 1.16 | -43.7% | 0.97 |
| BTC tendência + carry no caixa | 2020–2022 | 51.1% | 43.0% | 1.17 | -43.7% | 1.17 |
| BTC tendência + carry no caixa | 2023–2026 | 36.1% | 30.2% | 1.17 | -25.4% | 1.42 |
| BTC carry puro (1× capital) | 2020–2026 | 12.2% | 1.4% | 8.36 | -2.3% | 5.21 |
| BTC carry puro (1× capital) | 2020–2022 | 18.5% | 1.9% | 9.02 | -2.3% | 7.93 |
| BTC carry puro (1× capital) | 2023–2026 | 7.4% | 0.7% | 10.46 | -0.5% | 14.71 |
| BTC carry puro (1,5× capital) | 2020–2026 | 8.0% | 0.9% | 8.36 | -1.6% | 5.10 |
| BTC carry puro (1,5× capital) | 2020–2022 | 12.0% | 1.3% | 9.02 | -1.6% | 7.68 |
| BTC carry puro (1,5× capital) | 2023–2026 | 4.9% | 0.5% | 10.46 | -0.3% | 14.53 |
| ETH buy & hold | 2020–2026 | 51.9% | 80.4% | 0.93 | -79.3% | 0.65 |
| ETH buy & hold | 2020–2022 | 109.9% | 98.6% | 1.26 | -79.3% | 1.39 |
| ETH buy & hold | 2023–2026 | 18.0% | 62.6% | 0.57 | -67.6% | 0.27 |
| ETH tendência (caixa 0%) | 2020–2026 | 51.8% | 51.7% | 1.07 | -47.3% | 1.10 |
| ETH tendência (caixa 0%) | 2020–2022 | 103.7% | 66.2% | 1.41 | -47.3% | 2.19 |
| ETH tendência (caixa 0%) | 2023–2026 | 20.6% | 36.5% | 0.69 | -37.8% | 0.55 |
| ETH tendência + carry no caixa | 2020–2026 | 56.8% | 51.7% | 1.13 | -46.9% | 1.21 |
| ETH tendência + carry no caixa | 2020–2022 | 110.3% | 66.1% | 1.46 | -46.9% | 2.35 |
| ETH tendência + carry no caixa | 2023–2026 | 24.5% | 36.5% | 0.78 | -34.6% | 0.71 |
| ETH carry puro (1× capital) | 2020–2026 | 14.5% | 1.8% | 7.40 | -1.8% | 8.12 |
| ETH carry puro (1× capital) | 2020–2022 | 24.2% | 2.6% | 8.35 | -1.8% | 13.53 |
| ETH carry puro (1× capital) | 2023–2026 | 7.5% | 0.7% | 10.65 | -0.6% | 11.76 |
| ETH carry puro (1,5× capital) | 2020–2026 | 9.5% | 1.2% | 7.40 | -1.2% | 7.92 |
| ETH carry puro (1,5× capital) | 2020–2022 | 15.6% | 1.7% | 8.35 | -1.2% | 13.01 |
| ETH carry puro (1,5× capital) | 2023–2026 | 4.9% | 0.5% | 10.65 | -0.4% | 11.61 |


### 2b. Ano a ano — BTC

| ano | buy & hold | tendência | tendência + carry | carry puro |
|---|---|---|---|---|
| 2020 | 302% | 184% | 190% | 18% |
| 2021 | 60% | 55% | 63% | 36% |
| 2022 | -64% | -30% | -27% | 4% |
| 2023 | 156% | 77% | 82% | 8% |
| 2024 | 121% | 73% | 79% | 13% |
| 2025 | -6% | -5% | -2% | 5% |
| 2026 | -11% | 0% | 3% | 3% |


## 3. Momentum + Valor em ações brasileiras (NEFIN-USP, 2001–2026)

Long-only = 50% no terço de maior momentum + 50% no terço de maior valor patrimonial/preço, custo de giro de ~1% a.a. Long-short = 50% WML + 50% HML com colateral em Tesouro Selic (rende CDI), menos ~2% a.a. de giro e 1,5× a taxa média de aluguel de ações medida pelo NEFIN. Sharpe medido contra o CDI.

| estratégia | período | CAGR | vol | sharpe | maxDD | calmar |
|---|---|---|---|---|---|---|
| CDI | 2001–2026 | 12.1% | 0.3% | 0.00 | 0.0% | — |
| CDI | 2001–2013 | 14.0% | 0.3% | 0.00 | 0.0% | — |
| CDI | 2014–2026 | 10.1% | 0.2% | 0.00 | 0.0% | — |
| Mercado (índice NEFIN) | 2001–2026 | 13.5% | 23.9% | 0.17 | -57.3% | 0.24 |
| Mercado (índice NEFIN) | 2001–2013 | 16.2% | 25.8% | 0.20 | -57.3% | 0.28 |
| Mercado (índice NEFIN) | 2014–2026 | 10.9% | 21.9% | 0.14 | -45.0% | 0.24 |
| Só momentum alto (long-only) | 2001–2026 | 17.3% | 25.2% | 0.31 | -61.8% | 0.28 |
| Só momentum alto (long-only) | 2001–2013 | 18.9% | 26.4% | 0.29 | -61.8% | 0.31 |
| Só momentum alto (long-only) | 2014–2026 | 15.6% | 23.8% | 0.32 | -47.6% | 0.33 |
| Momentum + Valor long-only | 2001–2026 | 16.2% | 26.3% | 0.27 | -60.2% | 0.27 |
| Momentum + Valor long-only | 2001–2013 | 16.9% | 26.9% | 0.23 | -60.2% | 0.28 |
| Momentum + Valor long-only | 2014–2026 | 15.5% | 25.6% | 0.32 | -50.5% | 0.31 |
| CDI + Momentum/Valor long-short | 2001–2026 | 15.2% | 13.5% | 0.27 | -29.1% | 0.52 |
| CDI + Momentum/Valor long-short | 2001–2013 | 10.9% | 12.6% | -0.16 | -29.1% | 0.38 |
| CDI + Momentum/Valor long-short | 2014–2026 | 19.8% | 14.4% | 0.66 | -19.5% | 1.02 |


### 3b. Ano a ano

| ano | CDI | Mercado (índice NEFIN) | Só momentum alto (long-only) | Momentum + Valor long-only | CDI + Momentum/Valor long-short |
|---|---|---|---|---|---|
| 2001 | 18% | 1% | -5% | 4% | 21% |
| 2002 | 19% | 4% | 14% | 9% | 23% |
| 2003 | 23% | 77% | 47% | 81% | 15% |
| 2004 | 16% | 27% | 58% | 43% | 36% |
| 2005 | 19% | 33% | 29% | 23% | 18% |
| 2006 | 15% | 33% | 33% | 32% | 8% |
| 2007 | 11% | 43% | 53% | 42% | 17% |
| 2008 | 12% | -39% | -44% | -40% | 5% |
| 2009 | 10% | 74% | 60% | 59% | -17% |
| 2010 | 10% | 6% | 22% | 11% | 12% |
| 2011 | 12% | -7% | 11% | -3% | 13% |
| 2012 | 8% | 13% | 27% | 16% | 5% |
| 2013 | 8% | -3% | -11% | -8% | -6% |
| 2014 | 11% | -4% | -1% | -16% | -1% |
| 2015 | 13% | -12% | -5% | -16% | 16% |
| 2016 | 14% | 36% | 25% | 62% | 30% |
| 2017 | 10% | 27% | 34% | 28% | 12% |
| 2018 | 6% | 15% | 13% | 23% | 31% |
| 2019 | 6% | 35% | 35% | 39% | 7% |
| 2020 | 3% | 4% | 40% | 16% | 11% |
| 2021 | 5% | -10% | -1% | 1% | 41% |
| 2022 | 13% | 1% | 5% | 8% | 42% |
| 2023 | 13% | 25% | 27% | 39% | 37% |
| 2024 | 11% | -8% | 5% | -4% | 22% |
| 2025 | 14% | 30% | 19% | 31% | 11% |
| 2026 | 10% | 14% | 10% | 8% | 1% |

