# Resultados — Day trade em cripto (dados de 1 minuto)

Carteira igual entre BTC, ETH, SOL, DOGE e XRP (perpétuos Binance). Custos por lado: 0,06% (BTC/ETH) e 0,07% (demais) = taxa agressora VIP0 + slippage; funding real a cada 8h. `bruto` = sem custos; `fade` = sinal invertido. IS = 2020–2023; OOS = 2024–out/2026.

## K1. Resumo OOS (2024–2026) — carteira dos 5 ativos

| estratégia | bruto: média/mês | bruto: sharpe | líquido: média/mês | líquido: sharpe | fade: média/mês | fade: sharpe |
|---|---|---|---|---|---|---|
| Cruzamento MME 9/21 (5m) | -1.8% | -0.29 | -43.3% | -12.10 | -42.9% | -14.13 |
| Cruzamento MME 9/21 (15m) | +1.4% | 0.45 | -15.1% | -3.59 | -19.1% | -5.22 |
| MACD 12/26/9 (15m) | -4.2% | -0.88 | -29.5% | -7.38 | -24.4% | -6.58 |
| RSI 14: compra <30, vende >70 (5m) | +2.6% | 0.97 | -11.9% | -4.50 | -17.3% | -6.68 |
| RSI 14: compra <30, vende >70 (15m) | -1.1% | -0.29 | -6.0% | -2.17 | -4.9% | -1.73 |
| Bollinger 20,2 reversão (5m) | +4.0% | 1.22 | -30.9% | -10.88 | -37.2% | -12.86 |
| Preço vs VWAP do dia (15m) | +0.5% | 0.20 | -34.0% | -8.12 | -35.9% | -10.96 |
| Supertrend 10,3 (15m) | +2.1% | 0.55 | -6.3% | -1.46 | -11.5% | -2.92 |
| Supertrend 10,3 (1h) | +0.8% | 0.27 | -1.4% | -0.22 | -3.9% | -0.85 |
| Setup 9.1 Larry Williams (15m) | -3.1% | -0.64 | -57.4% | -17.97 | -55.6% | -21.53 |
| Setup 9.1 Larry Williams (1h) | +0.8% | 0.30 | -17.1% | -4.01 | -19.6% | -5.25 |
| ORB abertura de NY (1m) | +0.4% | 0.21 | -3.5% | -1.55 | -4.5% | -2.03 |
| Rompimento máx/mín do dia anterior (1m) | -0.7% | -0.22 | -3.9% | -1.08 | -3.1% | -0.87 |
| ICT liquidity sweep (5m) | +0.3% | 0.16 | -4.2% | -1.88 | -5.2% | -2.28 |
| Scalping de spike >4σ (1m) | -0.6% | -0.40 | -21.0% | -13.24 | -20.2% | -12.50 |
| Rompimento de volatilidade k=0,5 (diário) | +2.3% | 0.87 | +0.7% | 0.25 | -3.8% | -1.49 |


## K2. Tabela completa (carteira), IS e OOS

| estratégia | modo | período | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês |
|---|---|---|---|---|---|---|---|---|---|
| Cruzamento MME 9/21 (5m) | bruto | total | -47.5% | -0.74 | -99.1% | -3.6% | -4.8% | 22% | -44.6% |
| Cruzamento MME 9/21 (5m) | bruto | IS 2020–2023 | -59.4% | -0.98 | -98.2% | -4.8% | -7.4% | 19% | -44.6% |
| Cruzamento MME 9/21 (5m) | bruto | OOS 2024–2026 | -24.4% | -0.29 | -71.4% | -1.8% | -2.7% | 26% | -19.2% |
| Cruzamento MME 9/21 (5m) | líquido | total | -99.9% | -10.82 | -100.0% | -44.7% | -45.4% | 1% | -69.5% |
| Cruzamento MME 9/21 (5m) | líquido | IS 2020–2023 | -100.0% | -10.27 | -100.0% | -45.7% | -46.7% | 2% | -69.5% |
| Cruzamento MME 9/21 (5m) | líquido | OOS 2024–2026 | -99.9% | -12.10 | -100.0% | -43.3% | -42.6% | 0% | -54.5% |
| Cruzamento MME 9/21 (5m) | fade líquido | total | -99.9% | -11.78 | -100.0% | -42.2% | -42.4% | 0% | -78.0% |
| Cruzamento MME 9/21 (5m) | fade líquido | IS 2020–2023 | -99.9% | -10.65 | -100.0% | -41.7% | -42.1% | 0% | -78.0% |
| Cruzamento MME 9/21 (5m) | fade líquido | OOS 2024–2026 | -99.9% | -14.13 | -100.0% | -42.9% | -43.0% | 0% | -52.3% |
| Cruzamento MME 9/21 (15m) | bruto | total | -19.9% | -0.00 | -93.6% | -1.1% | -0.7% | 24% | -25.1% |
| Cruzamento MME 9/21 (15m) | bruto | IS 2020–2023 | -36.4% | -0.20 | -91.0% | -2.9% | -3.4% | 19% | -25.1% |
| Cruzamento MME 9/21 (15m) | bruto | OOS 2024–2026 | 10.9% | 0.45 | -38.0% | 1.4% | 0.9% | 32% | -22.6% |
| Cruzamento MME 9/21 (15m) | líquido | total | -91.0% | -3.05 | -100.0% | -17.5% | -17.7% | 4% | -38.0% |
| Cruzamento MME 9/21 (15m) | líquido | IS 2020–2023 | -93.2% | -2.90 | -100.0% | -19.3% | -20.2% | 6% | -38.0% |
| Cruzamento MME 9/21 (15m) | líquido | OOS 2024–2026 | -86.9% | -3.59 | -99.7% | -15.1% | -15.4% | 0% | -36.0% |
| Cruzamento MME 9/21 (15m) | fade líquido | total | -91.9% | -3.96 | -100.0% | -18.3% | -18.5% | 0% | -42.1% |
| Cruzamento MME 9/21 (15m) | fade líquido | IS 2020–2023 | -91.3% | -3.38 | -100.0% | -17.6% | -17.4% | 0% | -42.1% |
| Cruzamento MME 9/21 (15m) | fade líquido | OOS 2024–2026 | -92.6% | -5.22 | -99.9% | -19.1% | -19.0% | 0% | -32.2% |
| MACD 12/26/9 (15m) | bruto | total | -55.8% | -1.03 | -99.8% | -5.2% | -5.7% | 21% | -45.3% |
| MACD 12/26/9 (15m) | bruto | IS 2020–2023 | -61.7% | -1.12 | -98.6% | -5.9% | -6.8% | 23% | -45.3% |
| MACD 12/26/9 (15m) | bruto | OOS 2024–2026 | -45.8% | -0.88 | -85.8% | -4.2% | -4.3% | 18% | -22.9% |
| MACD 12/26/9 (15m) | líquido | total | -98.9% | -6.72 | -100.0% | -30.1% | -31.1% | 1% | -60.7% |
| MACD 12/26/9 (15m) | líquido | IS 2020–2023 | -99.0% | -6.39 | -100.0% | -30.6% | -31.9% | 2% | -60.7% |
| MACD 12/26/9 (15m) | líquido | OOS 2024–2026 | -98.7% | -7.38 | -100.0% | -29.5% | -30.5% | 0% | -44.5% |
| MACD 12/26/9 (15m) | fade líquido | total | -96.9% | -5.75 | -100.0% | -24.0% | -24.8% | 2% | -64.7% |
| MACD 12/26/9 (15m) | fade líquido | IS 2020–2023 | -96.9% | -5.32 | -100.0% | -23.7% | -23.4% | 4% | -64.7% |
| MACD 12/26/9 (15m) | fade líquido | OOS 2024–2026 | -96.8% | -6.58 | -100.0% | -24.4% | -25.5% | 0% | -45.6% |
| RSI 14: compra <30, vende >70 (5m) | bruto | total | 48.7% | 1.18 | -32.5% | 3.7% | 4.1% | 44% | -21.2% |
| RSI 14: compra <30, vende >70 (5m) | bruto | IS 2020–2023 | 62.5% | 1.30 | -32.2% | 4.5% | 4.6% | 48% | -21.2% |
| RSI 14: compra <30, vende >70 (5m) | bruto | OOS 2024–2026 | 31.1% | 0.97 | -32.5% | 2.6% | 2.9% | 38% | -18.1% |
| RSI 14: compra <30, vende >70 (5m) | líquido | total | -74.7% | -3.16 | -100.0% | -10.5% | -10.2% | 1% | -30.7% |
| RSI 14: compra <30, vende >70 (5m) | líquido | IS 2020–2023 | -71.1% | -2.51 | -99.3% | -9.5% | -9.5% | 2% | -30.7% |
| RSI 14: compra <30, vende >70 (5m) | líquido | OOS 2024–2026 | -79.0% | -4.50 | -98.8% | -11.9% | -11.8% | 0% | -28.7% |
| RSI 14: compra <30, vende >70 (5m) | fade líquido | total | -91.7% | -5.58 | -100.0% | -18.3% | -18.3% | 2% | -45.5% |
| RSI 14: compra <30, vende >70 (5m) | fade líquido | IS 2020–2023 | -92.6% | -5.16 | -100.0% | -19.1% | -19.3% | 2% | -45.5% |
| RSI 14: compra <30, vende >70 (5m) | fade líquido | OOS 2024–2026 | -90.1% | -6.68 | -99.9% | -17.3% | -17.3% | 3% | -28.5% |
| RSI 14: compra <30, vende >70 (15m) | bruto | total | -3.7% | 0.12 | -46.6% | 0.1% | -0.6% | 26% | -28.3% |
| RSI 14: compra <30, vende >70 (15m) | bruto | IS 2020–2023 | 4.3% | 0.33 | -46.6% | 0.9% | 2.5% | 29% | -28.3% |
| RSI 14: compra <30, vende >70 (15m) | bruto | OOS 2024–2026 | -14.0% | -0.29 | -46.2% | -1.1% | -1.3% | 21% | -13.8% |
| RSI 14: compra <30, vende >70 (15m) | líquido | total | -47.3% | -1.38 | -98.8% | -4.8% | -5.6% | 7% | -31.5% |
| RSI 14: compra <30, vende >70 (15m) | líquido | IS 2020–2023 | -42.6% | -1.00 | -91.3% | -4.0% | -2.4% | 12% | -31.5% |
| RSI 14: compra <30, vende >70 (15m) | líquido | OOS 2024–2026 | -53.3% | -2.17 | -88.4% | -6.0% | -6.2% | 0% | -18.2% |
| RSI 14: compra <30, vende >70 (15m) | fade líquido | total | -55.2% | -1.51 | -99.7% | -6.1% | -5.8% | 9% | -37.2% |
| RSI 14: compra <30, vende >70 (15m) | fade líquido | IS 2020–2023 | -60.5% | -1.47 | -98.0% | -6.9% | -8.2% | 12% | -37.2% |
| RSI 14: compra <30, vende >70 (15m) | fade líquido | OOS 2024–2026 | -46.5% | -1.73 | -84.1% | -4.9% | -4.5% | 3% | -15.4% |
| Bollinger 20,2 reversão (5m) | bruto | total | 87.0% | 1.56 | -49.3% | 6.0% | 5.3% | 51% | -31.8% |
| Bollinger 20,2 reversão (5m) | bruto | IS 2020–2023 | 115.6% | 1.76 | -49.3% | 7.4% | 6.5% | 56% | -31.8% |
| Bollinger 20,2 reversão (5m) | bruto | OOS 2024–2026 | 52.9% | 1.22 | -28.4% | 4.0% | 3.6% | 44% | -12.0% |
| Bollinger 20,2 reversão (5m) | líquido | total | -98.6% | -9.06 | -100.0% | -29.7% | -30.0% | 0% | -55.3% |
| Bollinger 20,2 reversão (5m) | líquido | IS 2020–2023 | -98.5% | -8.09 | -100.0% | -28.9% | -29.4% | 0% | -55.3% |
| Bollinger 20,2 reversão (5m) | líquido | OOS 2024–2026 | -98.9% | -10.88 | -100.0% | -30.9% | -30.2% | 0% | -41.9% |
| Bollinger 20,2 reversão (5m) | fade líquido | total | -99.8% | -11.82 | -100.0% | -38.9% | -38.4% | 0% | -57.4% |
| Bollinger 20,2 reversão (5m) | fade líquido | IS 2020–2023 | -99.8% | -11.35 | -100.0% | -40.1% | -39.5% | 0% | -57.4% |
| Bollinger 20,2 reversão (5m) | fade líquido | OOS 2024–2026 | -99.6% | -12.86 | -100.0% | -37.2% | -36.9% | 0% | -45.5% |
| Preço vs VWAP do dia (15m) | bruto | total | 23.2% | 0.63 | -71.3% | 3.2% | -1.5% | 30% | -25.3% |
| Preço vs VWAP do dia (15m) | bruto | IS 2020–2023 | 46.6% | 0.85 | -68.0% | 5.2% | 1.6% | 35% | -25.3% |
| Preço vs VWAP do dia (15m) | bruto | OOS 2024–2026 | -3.6% | 0.20 | -64.0% | 0.5% | -3.5% | 24% | -24.9% |
| Preço vs VWAP do dia (15m) | líquido | total | -99.2% | -6.06 | -100.0% | -32.0% | -36.4% | 1% | -52.3% |
| Preço vs VWAP do dia (15m) | líquido | IS 2020–2023 | -99.1% | -5.13 | -100.0% | -30.5% | -35.0% | 2% | -51.8% |
| Preço vs VWAP do dia (15m) | líquido | OOS 2024–2026 | -99.4% | -8.12 | -100.0% | -34.0% | -37.3% | 0% | -52.3% |
| Preço vs VWAP do dia (15m) | fade líquido | total | -99.7% | -9.61 | -100.0% | -37.8% | -37.0% | 0% | -77.9% |
| Preço vs VWAP do dia (15m) | fade líquido | IS 2020–2023 | -99.8% | -9.06 | -100.0% | -39.1% | -37.9% | 0% | -77.9% |
| Preço vs VWAP do dia (15m) | fade líquido | OOS 2024–2026 | -99.6% | -10.96 | -100.0% | -35.9% | -35.6% | 0% | -55.8% |
| Supertrend 10,3 (15m) | bruto | total | -43.1% | -0.57 | -99.5% | -3.4% | -3.6% | 28% | -51.4% |
| Supertrend 10,3 (15m) | bruto | IS 2020–2023 | -65.7% | -1.15 | -99.2% | -7.4% | -4.5% | 17% | -51.4% |
| Supertrend 10,3 (15m) | bruto | OOS 2024–2026 | 16.7% | 0.55 | -61.4% | 2.1% | 2.1% | 44% | -25.9% |
| Supertrend 10,3 (15m) | líquido | total | -79.0% | -2.09 | -100.0% | -11.1% | -11.1% | 11% | -55.7% |
| Supertrend 10,3 (15m) | líquido | IS 2020–2023 | -87.0% | -2.45 | -100.0% | -14.5% | -12.4% | 8% | -55.7% |
| Supertrend 10,3 (15m) | líquido | OOS 2024–2026 | -58.8% | -1.46 | -92.9% | -6.3% | -6.8% | 15% | -32.3% |
| Supertrend 10,3 (15m) | fade líquido | total | -63.6% | -1.36 | -99.9% | -7.2% | -8.2% | 18% | -36.5% |
| Supertrend 10,3 (15m) | fade líquido | IS 2020–2023 | -46.3% | -0.58 | -92.2% | -4.2% | -6.8% | 25% | -28.9% |
| Supertrend 10,3 (15m) | fade líquido | OOS 2024–2026 | -78.9% | -2.92 | -98.8% | -11.5% | -12.7% | 9% | -36.5% |
| Supertrend 10,3 (1h) | bruto | total | -8.5% | 0.19 | -78.6% | 0.1% | -1.2% | 34% | -32.8% |
| Supertrend 10,3 (1h) | bruto | IS 2020–2023 | -14.2% | 0.15 | -71.7% | -0.4% | -1.1% | 31% | -21.6% |
| Supertrend 10,3 (1h) | bruto | OOS 2024–2026 | 0.2% | 0.27 | -40.0% | 0.8% | -1.4% | 38% | -32.8% |
| Supertrend 10,3 (1h) | líquido | total | -28.4% | -0.17 | -94.3% | -1.9% | -3.1% | 28% | -34.6% |
| Supertrend 10,3 (1h) | líquido | IS 2020–2023 | -31.9% | -0.15 | -88.2% | -2.3% | -2.9% | 25% | -23.2% |
| Supertrend 10,3 (1h) | líquido | OOS 2024–2026 | -23.1% | -0.22 | -58.1% | -1.4% | -3.5% | 32% | -34.6% |
| Supertrend 10,3 (1h) | fade líquido | total | -45.7% | -0.63 | -98.7% | -4.1% | -4.0% | 24% | -36.5% |
| Supertrend 10,3 (1h) | fade líquido | IS 2020–2023 | -47.0% | -0.53 | -94.7% | -4.3% | -4.9% | 29% | -36.5% |
| Supertrend 10,3 (1h) | fade líquido | OOS 2024–2026 | -43.8% | -0.85 | -85.0% | -3.9% | -2.5% | 18% | -21.8% |
| Setup 9.1 Larry Williams (15m) | bruto | total | -53.3% | -0.90 | -99.6% | -4.5% | -6.5% | 23% | -43.2% |
| Setup 9.1 Larry Williams (15m) | bruto | IS 2020–2023 | -62.3% | -1.05 | -98.1% | -5.5% | -7.0% | 25% | -43.2% |
| Setup 9.1 Larry Williams (15m) | bruto | OOS 2024–2026 | -36.6% | -0.64 | -80.9% | -3.1% | -6.1% | 21% | -21.3% |
| Setup 9.1 Larry Williams (15m) | líquido | total | -100.0% | -15.50 | -100.0% | -58.4% | -59.8% | 0% | -77.4% |
| Setup 9.1 Larry Williams (15m) | líquido | IS 2020–2023 | -100.0% | -14.41 | -100.0% | -59.1% | -60.2% | 0% | -77.4% |
| Setup 9.1 Larry Williams (15m) | líquido | OOS 2024–2026 | -100.0% | -17.97 | -100.0% | -57.4% | -58.8% | 0% | -66.7% |
| Setup 9.1 Larry Williams (15m) | fade líquido | total | -100.0% | -17.77 | -100.0% | -55.3% | -55.5% | 0% | -76.8% |
| Setup 9.1 Larry Williams (15m) | fade líquido | IS 2020–2023 | -100.0% | -16.04 | -100.0% | -55.1% | -55.5% | 0% | -76.8% |
| Setup 9.1 Larry Williams (15m) | fade líquido | OOS 2024–2026 | -100.0% | -21.53 | -100.0% | -55.6% | -55.5% | 0% | -65.3% |
| Setup 9.1 Larry Williams (1h) | bruto | total | -16.2% | 0.08 | -88.4% | -0.5% | -0.5% | 28% | -26.4% |
| Setup 9.1 Larry Williams (1h) | bruto | IS 2020–2023 | -27.2% | -0.02 | -80.4% | -1.4% | -2.0% | 27% | -26.4% |
| Setup 9.1 Larry Williams (1h) | bruto | OOS 2024–2026 | 2.1% | 0.30 | -63.6% | 0.8% | 1.0% | 29% | -24.6% |
| Setup 9.1 Larry Williams (1h) | líquido | total | -92.5% | -3.20 | -100.0% | -18.6% | -19.2% | 1% | -41.3% |
| Setup 9.1 Larry Williams (1h) | líquido | IS 2020–2023 | -93.8% | -2.93 | -100.0% | -19.7% | -20.8% | 2% | -41.3% |
| Setup 9.1 Larry Williams (1h) | líquido | OOS 2024–2026 | -90.3% | -4.01 | -99.9% | -17.1% | -16.6% | 0% | -38.8% |
| Setup 9.1 Larry Williams (1h) | fade líquido | total | -93.2% | -4.09 | -100.0% | -19.4% | -20.1% | 2% | -57.6% |
| Setup 9.1 Larry Williams (1h) | fade líquido | IS 2020–2023 | -93.2% | -3.58 | -100.0% | -19.2% | -20.6% | 4% | -57.6% |
| Setup 9.1 Larry Williams (1h) | fade líquido | OOS 2024–2026 | -93.2% | -5.25 | -100.0% | -19.6% | -19.7% | 0% | -34.6% |
| ORB abertura de NY (1m) | bruto | total | 7.2% | 0.39 | -47.1% | 0.9% | 0.2% | 27% | -20.6% |
| ORB abertura de NY (1m) | bruto | IS 2020–2023 | 10.9% | 0.50 | -47.1% | 1.3% | 0.1% | 31% | -20.6% |
| ORB abertura de NY (1m) | bruto | OOS 2024–2026 | 2.2% | 0.21 | -36.4% | 0.4% | 0.2% | 21% | -15.9% |
| ORB abertura de NY (1m) | líquido | total | -33.6% | -1.32 | -94.5% | -3.0% | -3.7% | 16% | -23.7% |
| ORB abertura de NY (1m) | líquido | IS 2020–2023 | -31.2% | -1.17 | -80.9% | -2.7% | -3.8% | 19% | -23.7% |
| ORB abertura de NY (1m) | líquido | OOS 2024–2026 | -36.9% | -1.55 | -74.1% | -3.5% | -3.7% | 12% | -19.1% |
| ORB abertura de NY (1m) | fade líquido | total | -48.1% | -2.23 | -98.9% | -5.0% | -4.6% | 9% | -19.9% |
| ORB abertura de NY (1m) | fade líquido | IS 2020–2023 | -50.7% | -2.37 | -94.1% | -5.4% | -4.8% | 8% | -19.9% |
| ORB abertura de NY (1m) | fade líquido | OOS 2024–2026 | -44.2% | -2.03 | -81.3% | -4.5% | -4.5% | 9% | -19.3% |
| Rompimento máx/mín do dia anterior (1m) | bruto | total | -1.3% | 0.26 | -82.1% | 1.0% | 0.5% | 28% | -31.3% |
| Rompimento máx/mín do dia anterior (1m) | bruto | IS 2020–2023 | 12.3% | 0.48 | -67.9% | 2.2% | 1.3% | 25% | -31.3% |
| Rompimento máx/mín do dia anterior (1m) | bruto | OOS 2024–2026 | -17.7% | -0.22 | -55.6% | -0.7% | -0.6% | 32% | -27.2% |
| Rompimento máx/mín do dia anterior (1m) | líquido | total | -31.7% | -0.36 | -97.2% | -2.1% | -2.7% | 23% | -33.4% |
| Rompimento máx/mín do dia anterior (1m) | líquido | IS 2020–2023 | -21.6% | -0.04 | -85.9% | -0.8% | -1.5% | 19% | -33.4% |
| Rompimento máx/mín do dia anterior (1m) | líquido | OOS 2024–2026 | -43.9% | -1.08 | -81.5% | -3.9% | -3.7% | 29% | -29.4% |
| Rompimento máx/mín do dia anterior (1m) | fade líquido | total | -54.1% | -1.16 | -99.6% | -5.3% | -5.9% | 21% | -44.0% |
| Rompimento máx/mín do dia anterior (1m) | fade líquido | IS 2020–2023 | -62.6% | -1.32 | -98.5% | -6.8% | -7.8% | 15% | -44.0% |
| Rompimento máx/mín do dia anterior (1m) | fade líquido | OOS 2024–2026 | -38.8% | -0.87 | -86.1% | -3.1% | -4.5% | 29% | -25.8% |
| ICT liquidity sweep (5m) | bruto | total | -14.3% | -0.28 | -79.5% | -0.8% | -1.0% | 27% | -44.7% |
| ICT liquidity sweep (5m) | bruto | IS 2020–2023 | -23.4% | -0.51 | -78.8% | -1.5% | -1.4% | 27% | -44.7% |
| ICT liquidity sweep (5m) | bruto | OOS 2024–2026 | 0.5% | 0.16 | -36.5% | 0.3% | -0.9% | 26% | -9.1% |
| ICT liquidity sweep (5m) | líquido | total | -49.6% | -1.86 | -99.2% | -5.1% | -5.2% | 7% | -47.3% |
| ICT liquidity sweep (5m) | líquido | IS 2020–2023 | -54.4% | -1.89 | -96.2% | -5.7% | -5.2% | 6% | -47.3% |
| ICT liquidity sweep (5m) | líquido | OOS 2024–2026 | -42.1% | -1.88 | -82.6% | -4.2% | -5.2% | 9% | -13.2% |
| ICT liquidity sweep (5m) | fade líquido | total | -40.4% | -1.25 | -97.4% | -3.6% | -4.5% | 10% | -23.0% |
| ICT liquidity sweep (5m) | fade líquido | IS 2020–2023 | -33.8% | -0.81 | -82.9% | -2.5% | -4.8% | 17% | -23.0% |
| ICT liquidity sweep (5m) | fade líquido | OOS 2024–2026 | -48.5% | -2.28 | -85.0% | -5.2% | -4.3% | 0% | -21.5% |
| Scalping de spike >4σ (1m) | bruto | total | 0.7% | 0.15 | -41.2% | 0.3% | 1.3% | 28% | -23.0% |
| Scalping de spike >4σ (1m) | bruto | IS 2020–2023 | 8.6% | 0.44 | -39.0% | 1.0% | 1.9% | 33% | -23.0% |
| Scalping de spike >4σ (1m) | bruto | OOS 2024–2026 | -9.3% | -0.40 | -30.4% | -0.6% | 0.4% | 21% | -14.1% |
| Scalping de spike >4σ (1m) | líquido | total | -93.1% | -10.51 | -100.0% | -19.7% | -19.4% | 0% | -39.8% |
| Scalping de spike >4σ (1m) | líquido | IS 2020–2023 | -92.2% | -9.11 | -100.0% | -18.8% | -18.0% | 0% | -39.8% |
| Scalping de spike >4σ (1m) | líquido | OOS 2024–2026 | -94.3% | -13.24 | -100.0% | -21.0% | -22.0% | 0% | -32.5% |
| Scalping de spike >4σ (1m) | fade líquido | total | -93.8% | -10.61 | -100.0% | -20.4% | -20.5% | 0% | -33.3% |
| Scalping de spike >4σ (1m) | fade líquido | IS 2020–2023 | -93.9% | -9.72 | -100.0% | -20.5% | -20.6% | 0% | -33.3% |
| Scalping de spike >4σ (1m) | fade líquido | OOS 2024–2026 | -93.5% | -12.50 | -100.0% | -20.2% | -19.5% | 0% | -32.2% |
| Rompimento de volatilidade k=0,5 (diário) | bruto | total | 73.7% | 1.43 | -36.2% | 5.9% | 2.6% | 38% | -16.0% |
| Rompimento de volatilidade k=0,5 (diário) | bruto | IS 2020–2023 | 118.8% | 1.73 | -36.2% | 8.5% | 3.3% | 42% | -13.0% |
| Rompimento de volatilidade k=0,5 (diário) | bruto | OOS 2024–2026 | 25.3% | 0.87 | -30.4% | 2.3% | 2.1% | 32% | -16.0% |
| Rompimento de volatilidade k=0,5 (diário) | líquido | total | 43.6% | 1.01 | -46.2% | 4.3% | 0.9% | 33% | -17.4% |
| Rompimento de volatilidade k=0,5 (diário) | líquido | IS 2020–2023 | 81.4% | 1.37 | -46.2% | 6.8% | 2.0% | 38% | -14.5% |
| Rompimento de volatilidade k=0,5 (diário) | líquido | OOS 2024–2026 | 3.2% | 0.25 | -35.1% | 0.7% | 0.2% | 26% | -17.4% |
| Rompimento de volatilidade k=0,5 (diário) | fade líquido | total | -62.3% | -1.86 | -99.9% | -6.3% | -5.3% | 10% | -81.1% |
| Rompimento de volatilidade k=0,5 (diário) | fade líquido | IS 2020–2023 | -72.7% | -2.09 | -99.5% | -8.1% | -5.3% | 8% | -81.1% |
| Rompimento de volatilidade k=0,5 (diário) | fade líquido | OOS 2024–2026 | -40.5% | -1.49 | -79.7% | -3.8% | -5.2% | 12% | -29.7% |


## K3. As 15 melhores combinações estratégia×ativo no OOS (cuidado: escolher a melhor depois é viés de seleção)

| estratégia | modo | ativo | CAGR | sharpe | maxDD | média_mês | mediana_mês | %meses≥5% | pior_mês | trades/dia |
|---|---|---|---|---|---|---|---|---|---|---|
| Supertrend 10,3 (1h) | líquido | DOGE | 18.8% | 0.64 | -74.3% | 3.8% | -0.9% | 35% | -30.1% | 0.50 |
| Supertrend 10,3 (1h) | líquido | XRP | -9.1% | 0.27 | -72.6% | 1.3% | -2.1% | 32% | -34.7% | 0.50 |
| Supertrend 10,3 (1h) | fade líquido | SOL | -19.5% | 0.11 | -75.4% | 0.5% | -6.1% | 35% | -37.0% | 0.60 |
| Rompimento máx/mín do dia anterior (1m) | fade líquido | SOL | -21.2% | -0.04 | -74.6% | -0.4% | -6.6% | 32% | -26.9% | 1.60 |
| Supertrend 10,3 (1h) | fade líquido | BTC | -18.2% | -0.20 | -52.0% | -1.2% | -3.9% | 24% | -17.2% | 0.50 |
| ORB abertura de NY (1m) | líquido | ETH | -18.1% | -0.42 | -47.6% | -1.3% | -1.9% | 12% | -22.3% | 2.00 |
| Rompimento máx/mín do dia anterior (1m) | fade líquido | BTC | -28.6% | -0.69 | -73.1% | -2.2% | -3.7% | 29% | -21.4% | 1.50 |
| Supertrend 10,3 (1h) | fade líquido | ETH | -34.6% | -0.36 | -78.7% | -2.2% | -1.7% | 24% | -29.5% | 0.50 |
| Rompimento máx/mín do dia anterior (1m) | líquido | ETH | -35.0% | -0.53 | -72.3% | -2.5% | -4.8% | 32% | -33.3% | 1.60 |
| Rompimento máx/mín do dia anterior (1m) | líquido | XRP | -43.4% | -0.55 | -82.3% | -2.5% | -4.2% | 26% | -37.7% | 1.50 |
| ICT liquidity sweep (5m) | líquido | SOL | -33.5% | -0.64 | -75.6% | -2.6% | -4.2% | 29% | -19.0% | 2.30 |
| Supertrend 10,3 (1h) | líquido | ETH | -38.1% | -0.41 | -82.5% | -2.7% | -5.1% | 32% | -47.3% | 0.50 |
| Supertrend 10,3 (15m) | líquido | ETH | -36.3% | -0.36 | -81.9% | -2.8% | -2.6% | 18% | -31.7% | 2.00 |
| ORB abertura de NY (1m) | fade líquido | BTC | -31.6% | -1.60 | -66.2% | -3.0% | -2.7% | 3% | -15.4% | 2.00 |
| ORB abertura de NY (1m) | líquido | DOGE | -36.0% | -0.90 | -78.9% | -3.2% | -3.9% | 21% | -21.9% | 2.00 |

