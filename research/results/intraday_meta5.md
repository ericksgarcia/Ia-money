# Resultados — A meta de 5% ao mês

Período comum: 2022-01 a 2026-10. Sinais de posicionamento com 1h de atraso extra. Pesos da combinação (estimados em 2022–2023): Contra o varejo 20%, Top traders × varejo 34%, Cascata de liquidação 20%, Tendência + carry BTC (estudo 1) 26%.

## Q1. Desempenho sem alavancagem

| estratégia | período | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês |
|---|---|---|---|---|---|---|---|---|
| Contra o varejo | 2022–2023 | 34.0% | 1.04 | -24.6% | 2.9% | 3.6% | 46% | -12.5% |
| Contra o varejo | OOS 2024–2026 | 18.3% | 0.75 | -29.3% | 1.7% | 0.2% | 32% | -14.9% |
| Top traders × varejo | 2022–2023 | 28.8% | 1.36 | -10.2% | 2.2% | 0.0% | 21% | -3.2% |
| Top traders × varejo | OOS 2024–2026 | 21.8% | 0.88 | -26.7% | 1.9% | 0.4% | 24% | -9.3% |
| Cascata de liquidação | 2022–2023 | 9.8% | 0.44 | -32.4% | 1.1% | 0.6% | 33% | -18.6% |
| Cascata de liquidação | OOS 2024–2026 | 10.7% | 0.56 | -31.9% | 1.0% | 1.8% | 12% | -11.1% |
| Tendência + carry BTC (estudo 1) | 2022–2023 | 15.5% | 0.69 | -27.4% | 1.5% | -1.4% | 25% | -7.6% |
| Tendência + carry BTC (estudo 1) | OOS 2024–2026 | 22.6% | 0.84 | -25.4% | 2.2% | -0.7% | 21% | -12.7% |
| Combinação (paridade de risco) | 2022–2023 | 25.4% | 1.61 | -11.0% | 2.0% | 2.6% | 21% | -4.2% |
| Combinação (paridade de risco) | OOS 2024–2026 | 21.8% | 1.31 | -14.3% | 1.8% | 0.1% | 12% | -5.5% |


## Q2. Correlação entre as estratégias (diária, 2022–2026)

|  | Contra o varejo | Top traders × varejo | Cascata de liquidação | Tendência + carry BTC  |
|---|---|---|---|---|
| Contra o varejo | 1.00 | 0.46 | -0.06 | -0.11 |
| Top traders × varejo | 0.46 | 1.00 | -0.00 | 0.04 |
| Cascata de liquidação | -0.06 | -0.00 | 1.00 | 0.24 |
| Tendência + carry BTC (estudo 1) | -0.11 | 0.04 | 0.24 | 1.00 |


## Q3. Alavancagem necessária para 5% ao mês (com base no OOS 2024–2026)

| estratégia | média/mês 1× | alavancagem p/ 5%/mês (aritmético) | Kelly (ótimo teórico) | ½ Kelly (usual) |
|---|---|---|---|---|
| Contra o varejo | +1.72% | 2.9× | 2.7× | 1.4× |
| Top traders × varejo | +1.89% | 2.6× | 3.3× | 1.7× |
| Cascata de liquidação | +1.03% | 4.9× | 2.4× | 1.2× |
| Tendência + carry BTC (estudo 1) | +2.19% | 2.3× | 2.9× | 1.5× |
| Combinação (paridade de risco) | +1.79% | 2.8× | 8.1× | 4.1× |


Acima do Kelly, mais alavancagem **reduz** o crescimento esperado e aumenta a chance de ruína.

## Q4. Monte Carlo — 10.000 trajetórias de 12 meses (bootstrap em blocos de 10 dias dos retornos OOS 2024–2026)

### Combinação (paridade de risco)

| alavancagem | retorno 12m mediano | P(≥ +79,6% = 5%/mês) | P(queda ≥ 50% em algum momento) | P(ruína ≥ 95%) | P(terminar no prejuízo) |
|---|---|---|---|---|---|
| 1.0× | +22% | 2% | 0% | 0.0% | 11% |
| 2.0× | +43% | 27% | 0% | 0.0% | 14% |
| 2.8× | +63% | 42% | 4% | 0.0% | 14% |
| 3.0× | +67% | 44% | 6% | 0.0% | 15% |
| 5.0× | +102% | 56% | 43% | 0.0% | 20% |


### Contra o varejo

| alavancagem | retorno 12m mediano | P(≥ +79,6% = 5%/mês) | P(queda ≥ 50% em algum momento) | P(ruína ≥ 95%) | P(terminar no prejuízo) |
|---|---|---|---|---|---|
| 1.0× | +18% | 6% | 0% | 0.0% | 27% |
| 2.0× | +30% | 27% | 19% | 0.0% | 31% |
| 2.9× | +35% | 35% | 52% | 0.0% | 35% |
| 3.0× | +33% | 36% | 55% | 0.0% | 35% |
| 5.0× | +18% | 37% | 92% | 2.3% | 45% |


### Tendência + carry BTC (estudo 1)

| alavancagem | retorno 12m mediano | P(≥ +79,6% = 5%/mês) | P(queda ≥ 50% em algum momento) | P(ruína ≥ 95%) | P(terminar no prejuízo) |
|---|---|---|---|---|---|
| 1.0× | +21% | 10% | 0% | 0.0% | 25% |
| 2.0× | +35% | 31% | 19% | 0.0% | 30% |
| 2.3× | +38% | 35% | 30% | 0.0% | 31% |
| 3.0× | +41% | 39% | 57% | 0.0% | 35% |
| 5.0× | +19% | 38% | 96% | 2.0% | 45% |

