# Resultados — Ímãs de liquidação (reconstruídos do open interest)

`imb` > 0 = mais liquidações de vendidos acima do preço (combustível para alta) do que de comprados abaixo.

## W1. Retorno futuro conforme o lado do ímã (quintis definidos no IS)

| ativo | período | horizonte | ret. quando ímã ACIMA | ret. quando ímã ABAIXO | diferença | t (ajustado) |
|---|---|---|---|---|---|---|
| BTC | IS | 4h | +0.01% | +0.05% | -0.03% | -0.54 |
| BTC | IS | 24h | +0.07% | +0.20% | -0.13% | -0.34 |
| BTC | OOS | 4h | +0.02% | +0.01% | +0.01% | 0.36 |
| BTC | OOS | 24h | +0.10% | +0.06% | +0.03% | 0.13 |
| ETH | IS | 4h | -0.02% | -0.04% | +0.02% | 0.18 |
| ETH | IS | 24h | -0.10% | -0.16% | +0.06% | 0.11 |
| ETH | OOS | 4h | +0.03% | -0.04% | +0.07% | 1.37 |
| ETH | OOS | 24h | +0.09% | -0.18% | +0.27% | 0.87 |
| SOL | IS | 4h | +0.06% | +0.04% | +0.02% | 0.14 |
| SOL | IS | 24h | +0.27% | +0.02% | +0.24% | 0.29 |
| SOL | OOS | 4h | +0.03% | +0.02% | +0.02% | 0.23 |
| SOL | OOS | 24h | +0.05% | +0.10% | -0.06% | -0.15 |
| DOGE | IS | 4h | -0.07% | +0.06% | -0.14% | -1.12 |
| DOGE | IS | 24h | -0.02% | +0.19% | -0.21% | -0.30 |
| DOGE | OOS | 4h | +0.09% | -0.01% | +0.10% | 1.34 |
| DOGE | OOS | 24h | +0.54% | -0.05% | +0.59% | 1.34 |
| XRP | IS | 4h | -0.03% | -0.01% | -0.01% | -0.14 |
| XRP | IS | 24h | -0.12% | -0.13% | +0.01% | 0.02 |
| XRP | OOS | 4h | +0.14% | +0.06% | +0.08% | 1.09 |
| XRP | OOS | 24h | +0.53% | +0.18% | +0.34% | 0.80 |


## W2. Estratégia (carteira dos 5 ativos, 24 tranches, custos + funding)

| estratégia | período | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês |
|---|---|---|---|---|---|---|---|---|
| Ímã de liquidação · a favor do ímã | total | -14.2% | -0.37 | -75.2% | -0.9% | -1.7% | 22% | -27.4% |
| Ímã de liquidação · a favor do ímã | IS 2020–2023 | -27.1% | -0.89 | -71.7% | -2.1% | -2.2% | 18% | -27.4% |
| Ímã de liquidação · a favor do ímã | OOS 2024–2026 | 1.8% | 0.20 | -32.9% | 0.4% | -1.0% | 26% | -11.8% |
| Ímã de liquidação · contra o ímã | total | -20.1% | -0.63 | -80.0% | -1.5% | -0.9% | 14% | -19.0% |
| Ímã de liquidação · contra o ímã | IS 2020–2023 | -6.3% | -0.06 | -35.6% | -0.1% | -0.3% | 18% | -16.7% |
| Ímã de liquidação · contra o ímã | OOS 2024–2026 | -32.5% | -1.28 | -72.1% | -3.0% | -1.6% | 9% | -19.0% |

