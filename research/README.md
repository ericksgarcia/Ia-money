# research/

Código dos estudos. Conclusões em [`docs/ESTUDO_ESTRATEGIAS.md`](../docs/ESTUDO_ESTRATEGIAS.md) (diário) e [`docs/ESTUDO_INTRADAY.md`](../docs/ESTUDO_INTRADAY.md) (1 minuto).

## Reproduzir

```bash
pip install -r research/requirements.txt
bash research/data/fetch_github_data.sh /caminho/dados        # fatores EUA/Brasil, S&P/Shiller, BTC (repositórios do GitHub)
python research/data/download_binance.py /caminho/dados/binance  # 701 pares spot + funding de 924 perpétuos (~10 min)
export DATA_DIR=/caminho/dados
python research/strategies/acoes.py       # → results/acoes.md
python research/strategies/cripto.py      # → results/cripto.md
python research/strategies/finalistas.py  # → results/finalistas.md + gráficos
```

`download_binance.py` também baixa os candles diários dos perpétuos BTCUSDT/ETHUSDT (`perp_1d/`), usados para medir a base spot×perpétuo no carry.

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `lib.py` | Carregadores, métricas (CAGR, Sharpe, drawdown, Sharpe deflacionado) e execução de sinais com custo |
| `signals.py` | As 23 regras de tendência e a média entre elas (estratégia 1) |
| `strategies/acoes.py` | Fatores EUA/Brasil, timing de mercado e regras técnicas diárias |
| `strategies/cripto.py` | Tendência, reversão, cross-section, carry de funding, sazonalidade e candles |
| `strategies/finalistas.py` | Análise detalhada das 3 vencedoras |
| `results/` | Tabelas geradas e gráficos |

## Estudo 2 — intradiário (`intraday/`)

```bash
pip install pyarrow lightgbm openpyxl
python research/data/download_intraday.py /caminho/dados   # 1m + métricas 5m de BTC/ETH/SOL/DOGE/XRP (~1 GB)
python research/intraday/day_trade_cripto.py      # 15 setups populares + fade  → results/intraday_daytrade_cripto.md
python research/intraday/maker.py                 # contraparte com ordens limitadas → results/intraday_maker.md
python research/intraday/posicionamento.py        # contra o varejo, top traders, liquidações → results/intraday_posicionamento.md
python research/intraday/robustez_posicionamento.py
python research/intraday/spy.py                   # ORB, zona de ruído etc. no SPY 1m → results/intraday_spy.md
python research/intraday/win.py                   # setups brasileiros no WIN 5m → results/intraday_win.md
python research/intraday/ml.py                    # LightGBM walk-forward → results/intraday_ml.md
python research/intraday/meta5.py                 # alavancagem e Monte Carlo para 5%/mês → results/intraday_meta5.md
python research/intraday/graficos.py
```

| Arquivo | Conteúdo |
|---|---|
| `intraday/core.py` | Carregadores de 1m, reamostragem, motor com custos e funding, métricas mensais |
| `intraday/day_trade_cripto.py` | MME 9/21, MACD, RSI, Bollinger, VWAP, Supertrend, 9.1, ORB, PDH/PDL, ICT sweep, scalping, rompimento de volatilidade |
| `intraday/maker.py` | Simulação de ordens limitadas com execução por travessia (seleção adversa) |
| `intraday/posicionamento.py` | Razão long/short do varejo e dos top traders, fluxo agressor, OI/liquidações, funding, sazonalidade |
| `intraday/spy.py` / `intraday/win.py` | Day trade em ações (SPY 1m) e no mini-índice (WIN 5m) |
| `intraday/ml.py` | LightGBM com 25 variáveis, walk-forward mensal com purga |
| `intraday/meta5.py` | Combinação por paridade de risco, Kelly e Monte Carlo com alavancagem |
