# Passo 1 (v2): proposta de sistema de trading autônomo

> Status: **aguardando aprovação do operador**. Nenhum código de integração (corretora, Telegram) foi escrito.
> Base: [ESTUDO_ESTRATEGIAS.md](ESTUDO_ESTRATEGIAS.md) (≈ 250 variantes testadas em EUA 1926–2026, Brasil 2001–2026 e cripto 2011–2026).

## 1. Decisão

Implementar as 3 estratégias vencedoras do estudo:

| Módulo | Estratégia | Execução | Frequência |
|---|---|---|---|
| **A** | Tendência em BTC/ETH (média de 23 regras, comprado ou caixa) | 100% automática via API da corretora | Diária (00:10 UTC) |
| **B** | Carry de funding no caixa do módulo A (vende perpétuo na fração em caixa) | 100% automática, na mesma conta | Diária, junto com A |
| **C** | Momentum em ações da B3 (terço com maior retorno em 12 meses) | Sinal automático e execução manual sua (sem API gratuita na B3) | Mensal |

O módulo B só entra se a corretora escolhida oferecer perpétuo com margem unificada e aceitar chamadas dos servidores do GitHub. Sem isso, o módulo A roda sozinho com caixa em USDT (Sharpe 1,07 em vez de 1,17 em 2023–2026).

## 2. Arquitetura (custo zero: repositório público, GitHub Actions e APIs gratuitas)

```
GitHub Actions
├─ cripto-diario.yml   (cron 00:10 UTC, ~1 min)
│    1. baixa candles diários (API pública da corretora)
│    2. calcula as 23 regras → posição-alvo BTC/ETH (0–100%)
│    3. compara com a posição real; só opera se o desvio for > 5 p.p. (economiza custo)
│    4. ajusta o spot e/ou o hedge no perpétuo (módulo B)
│    5. grava o estado no branch `data` e manda um resumo no Telegram
├─ acoes-mensal.yml    (1º dia útil do mês)
│    ranking de momentum da B3 com dados gratuitos (cotações B3/CVM)
│    → lista de compras/vendas no Telegram e numa Issue do repositório
├─ saude.yml           (diário)
│    confere se o job rodou, se a posição bate com o alvo e o drawdown;
│    abre Issue e pausa tudo se algo sair do esperado ("kill switch")
└─ reestudo.yml        (mensal)
     reroda o backtest com os dados novos para detectar se a vantagem está sumindo
```

**Proteções obrigatórias:**
- chave de API **sem permissão de saque**;
- limite máximo de posição;
- *kill switch* por variável do repositório;
- **modo papel** (paper trading) por 2 a 4 semanas antes de usar dinheiro real.

## 3. Expectativa honesta

| Módulo | Histórico (fora da amostra) | Pior queda histórica | Observação |
|---|---|---|---|
| A + B (BTC) | 36% a.a. em 2023–2026 · Sharpe 1,17 | −25% (2023–26) / −44% (2020–26) | 2025–2026 ficou perto de zero (−2% e +3%) |
| A (50/50 BTC+ETH) | 27% a.a. em 2023–2026 · Sharpe 0,93 | −30% | ETH mais fraco que BTC no período recente |
| C (B3 long-only) | 15,6% a.a. em 2014–2026, contra 10,9% do mercado e 10,1% do CDI | −48% | Cai junto com a bolsa em crises |

**O sistema não gera dinheiro do nada: ele precisa do seu capital e pode perder parte dele.** O ganho esperado é proporcional ao valor alocado. Os números acima são de backtest.

## 4. Pontos a resolver no Passo 2

1. **Corretora de cripto:** precisa atender residentes no Brasil, ter API spot (e idealmente perpétuo com margem unificada) e aceitar chamadas de servidores nos EUA, onde rodam os runners do GitHub. A Binance respondeu **HTTP 451** daqui. Vou comparar as alternativas, ou propor um runner próprio.
2. **Telegram:** um bot gratuito para relatórios e alertas.
3. **Capital e limites:** quanto alocar, posição máxima e drawdown que dispara a pausa.
4. **Tributação:** registrar operações para o imposto (o sistema pode gerar o relatório mensal).
