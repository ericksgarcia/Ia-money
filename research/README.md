# research/

Código do estudo de estratégias. Conclusões em [`docs/ESTUDO_ESTRATEGIAS.md`](../docs/ESTUDO_ESTRATEGIAS.md).

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
