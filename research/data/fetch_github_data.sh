#!/usr/bin/env bash
# Baixa os históricos usados no estudo, todos hospedados em repositórios públicos do GitHub.
# Uso: bash research/data/fetch_github_data.sh [DATA_DIR]
set -euo pipefail
D="${1:-/home/user/rawdata}"
mkdir -p "$D"/{ff,nefin,shiller,btc}
raw="https://raw.githubusercontent.com"
media="https://media.githubusercontent.com/media"   # arquivos em Git LFS

# Fama-French (Ken French Data Library) — EUA, 1926+
curl -fsSL "$raw/ZhenHaoFu810/StataFlow/HEAD/research/data/public/finance/fama_french/ff3/F-F_Research_Data_Factors.csv" -o "$D/ff/ff3_monthly.csv"
curl -fsSL "$raw/ZhenHaoFu810/StataFlow/HEAD/research/data/public/finance/fama_french/ff5/F-F_Research_Data_5_Factors_2x3.csv" -o "$D/ff/ff5_monthly.csv"
for f in F-F_Momentum_Factor F-F_ST_Reversal_Factor F-F_LT_Reversal_Factor; do
  curl -fsSL "$raw/chdejager/taming-the-factor-zoo-a-recreation/HEAD/data/$f.csv" -o "$D/ff/$f.csv"
done
curl -fsSL "$media/fernando-duarte/ERP/HEAD/Input/Portfolios_Formed_on_BETA.csv" -o "$D/ff/Portfolios_Formed_on_BETA.csv"
curl -fsSL "$media/fernando-duarte/ERP/HEAD/Input/Portfolios_Formed_on_VAR.csv" -o "$D/ff/Portfolios_Formed_on_VAR.csv"
curl -fsSL "$media/fernando-duarte/ERP/HEAD/Input/F-F_Research_Data_Factors_daily.CSV" -o "$D/ff/ff3_daily.csv"

# NEFIN-USP — fatores de risco do mercado brasileiro, 2001+
for f in nefin_factors.csv nefin_factors_monthly.csv portfolio_by_momentum.csv portfolio_by_book_to_market.csv portfolio_by_size.csv portfolio_by_illiq.csv; do
  curl -fsSL "$raw/nefin/nefin.github.io/HEAD/static/nefindata/risk-factors/$f" -o "$D/nefin/$f"
done

curl -fsSL "$raw/nefin/nefin.github.io/HEAD/static/nefindata/short-interest/average_loan_fee.csv" -o "$D/nefin/average_loan_fee.csv"

# Shiller (S&P 500 mensal desde 1871: preço, dividendos, lucros, CAPE)
curl -fsSL "$raw/datasets/s-and-p-500/HEAD/data/data.csv" -o "$D/shiller/sp500_shiller.csv"

# Bitcoin diário desde 2011
curl -fsSL "$raw/rcaljouw/btc-price-history/HEAD/data/btc-usd-daily.csv" -o "$D/btc/btc-usd-daily.csv"
echo "ok -> $D"

# Intradiário (estudo 2): SPY 1 minuto 2008–2021 e mini-índice WIN 5 minutos (jun–out/2023)
mkdir -p "$D/intraday"
curl -fsSL "$media/CryonicArtist/Xlchedelic/HEAD/spy_1min_2008_2021_cleaned.parquet" -o "$D/intraday/SPY_1m.parquet" \
  || curl -fsSL "$raw/CryonicArtist/Xlchedelic/HEAD/spy_1min_2008_2021_cleaned.parquet" -o "$D/intraday/SPY_1m.parquet"
curl -fsSL "$raw/Bielhpp/MarketPrediction_WinfutBr-CandlestickChart/HEAD/winfut_5min.xlsx" -o "$D/intraday/WIN_5m.xlsx"
