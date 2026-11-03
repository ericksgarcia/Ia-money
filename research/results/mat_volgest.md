# Resultados — Volatilidade prevista e gestão de risco

## Y1. A volatilidade é previsível (modelo HAR, ajuste até 2023, teste 2024–2026)

| ativo | b_dia | b_semana | b_mês | R² OOS (log RV) | erro vs 'amanhã = hoje' |
|---|---|---|---|---|---|
| BTC | 0.44 | 0.39 | 0.08 | 0.35 | 73% |
| ETH | 0.46 | 0.37 | 0.11 | 0.34 | 75% |
| SOL | 0.61 | 0.22 | 0.07 | 0.43 | 80% |
| DOGE | 0.57 | 0.21 | 0.14 | 0.49 | 80% |
| XRP | 0.51 | 0.26 | 0.15 | 0.47 | 78% |


## Y3a. Critério de inclusão de novas estratégias (decidido só com dados até 2023: Sharpe > 0,5)

| candidata | Sharpe até 2023 | incluída? |
|---|---|---|
| Mineração (composto) | 1.46 | sim |


## Y2. Efeito da gestão por volatilidade (exposição = alvo / σ prevista)

| estratégia | versão | período | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês |
|---|---|---|---|---|---|---|---|---|---|
| Contra o varejo | sem gestão | até 2023 | 34.0% | 1.04 | -24.6% | 2.9% | 3.6% | 46% | -12.5% |
| Contra o varejo | sem gestão | OOS 2024–2026 | 18.3% | 0.75 | -29.3% | 1.7% | 0.2% | 32% | -14.9% |
| Contra o varejo | com gestão de vol. | até 2023 | 32.0% | 1.27 | -17.3% | 2.5% | 3.3% | 29% | -8.3% |
| Contra o varejo | com gestão de vol. | OOS 2024–2026 | 23.9% | 1.05 | -19.0% | 2.0% | 0.6% | 35% | -12.9% |
| Top traders × varejo | sem gestão | até 2023 | 28.8% | 1.36 | -10.2% | 2.2% | 0.0% | 21% | -3.2% |
| Top traders × varejo | sem gestão | OOS 2024–2026 | 21.8% | 0.88 | -26.7% | 1.9% | 0.4% | 24% | -9.3% |
| Top traders × varejo | com gestão de vol. | até 2023 | 22.1% | 1.07 | -16.2% | 1.7% | 0.0% | 21% | -3.9% |
| Top traders × varejo | com gestão de vol. | OOS 2024–2026 | 19.2% | 0.92 | -26.2% | 1.7% | 0.5% | 24% | -11.2% |
| Cascata de liquidação | sem gestão | até 2023 | 9.8% | 0.44 | -32.4% | 1.1% | 0.6% | 33% | -18.6% |
| Cascata de liquidação | sem gestão | OOS 2024–2026 | 10.7% | 0.56 | -31.9% | 1.0% | 1.8% | 12% | -11.1% |
| Cascata de liquidação | com gestão de vol. | até 2023 | 24.8% | 1.13 | -20.7% | 2.0% | 1.1% | 33% | -12.9% |
| Cascata de liquidação | com gestão de vol. | OOS 2024–2026 | 12.2% | 0.58 | -41.7% | 1.2% | 1.7% | 24% | -15.0% |
| Tendência + carry BTC (estudo 1) | sem gestão | até 2023 | 15.5% | 0.69 | -27.4% | 1.5% | -1.4% | 25% | -7.6% |
| Tendência + carry BTC (estudo 1) | sem gestão | OOS 2024–2026 | 22.6% | 0.84 | -25.4% | 2.2% | -0.7% | 21% | -12.7% |
| Tendência + carry BTC (estudo 1) | com gestão de vol. | até 2023 | 12.3% | 0.60 | -36.3% | 1.3% | -0.3% | 25% | -9.9% |
| Tendência + carry BTC (estudo 1) | com gestão de vol. | OOS 2024–2026 | 17.2% | 0.86 | -23.4% | 1.6% | -0.4% | 26% | -7.5% |
| Mineração (composto) | sem gestão | até 2023 | 39.9% | 1.46 | -15.8% | 3.1% | 1.5% | 33% | -12.5% |
| Mineração (composto) | sem gestão | OOS 2024–2026 | 12.7% | 0.61 | -37.8% | 1.5% | -0.2% | 21% | -9.8% |
| Mineração (composto) | com gestão de vol. | até 2023 | 32.6% | 1.41 | -12.6% | 2.4% | 1.1% | 25% | -6.7% |
| Mineração (composto) | com gestão de vol. | OOS 2024–2026 | 8.5% | 0.48 | -39.6% | 1.0% | -0.0% | 18% | -9.3% |
| Combinação | sem gestão | até 2023 | 29.0% | 1.87 | -8.1% | 2.2% | 2.1% | 21% | -3.4% |
| Combinação | sem gestão | OOS 2024–2026 | 20.3% | 1.26 | -17.1% | 1.7% | -0.1% | 21% | -6.0% |
| Combinação | com gestão de vol. | até 2023 | 36.3% | 1.92 | -11.2% | 2.6% | 2.5% | 25% | -5.8% |
| Combinação | com gestão de vol. | OOS 2024–2026 | 18.2% | 1.07 | -21.7% | 1.6% | -0.2% | 26% | -6.3% |


## Y3b. Meta de 5% ao mês com a combinação gerida por volatilidade

Pesos (estimados até 2023): Contra o varejo 16%, Top traders × varejo 26%, Cascata de liquidação 16%, Tendência + carry BTC (estudo 1) 21%, Mineração (composto) 21%.

Média mensal OOS sem alavancagem: +1.56%.

| alavancagem | retorno 12m mediano | P(≥ +79,6% = 5%/mês) | P(queda ≥ 50% em algum momento) | P(ruína ≥ 95%) | P(terminar no prejuízo) |
|---|---|---|---|---|---|
| 1.0× | +18% | 2% | 0% | 0.0% | 18% |
| 2.0× | +34% | 23% | 1% | 0.0% | 21% |
| 3.0× | +51% | 38% | 10% | 0.0% | 22% |
| 3.2× | +54% | 40% | 12% | 0.0% | 22% |


- 1.0×: 2022: +15%, 2023: +58%, 2024: +39%, 2025: +11%, 2026: +4% · queda máx. -22% · meses ≥5%: 26%

- 3.2×: 2022: +41%, 2023: +292%, 2024: +162%, 2025: +28%, 2026: +3% · queda máx. -58% · meses ≥5%: 45%
