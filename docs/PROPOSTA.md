# Passo 1 (v3): proposta de sistema de trading autônomo

> Status: **aguardando aprovação do operador**. Nenhum código de integração (corretora, Telegram) foi escrito.
> Base: [ESTUDO_ESTRATEGIAS.md](ESTUDO_ESTRATEGIAS.md) (≈ 250 variantes, dados diários desde 1926) e
> [ESTUDO_INTRADAY.md](ESTUDO_INTRADAY.md) (dados de 1 minuto, posicionamento do varejo e a meta de 5% ao mês) e
> [ESTUDO_MATEMATICO.md](ESTUDO_MATEMATICO.md) (Hurst, Fourier, Ornstein-Uhlenbeck, entropia, mineração de equações, volatilidade).
> Versões anteriores: [docs/arquivo/](arquivo).

## 1. Decisão

Uma carteira de 4 sinais pouco correlacionados em perpétuos de cripto, mais um sinal mensal de ações:

| Módulo | Sinal | Ativos | Frequência | OOS 2024–2026 (1×) |
|---|---|---|---|---|
| **A** | Tendência (média de 23 regras) + carry de funding no caixa | BTC (e ETH) | Diária | +2,2%/mês · Sharpe 0,84 |
| **B** | **Contra o varejo:** vende quando as contas estão anormalmente compradas, compra no inverso | BTC, ETH, SOL, DOGE, XRP | Horária, segura 24h | +1,7%/mês · Sharpe 0,75 |
| **C** | **Top traders comprando enquanto o varejo vende** (e vice-versa) | idem | Horária, segura 24h | +1,9%/mês · Sharpe 0,88 |
| **D** | **Compra após cascata de liquidação** (queda forte + open interest despencando) | idem | Horária, segura 24h | +1,0%/mês · Sharpe 0,56 |
| **A+B+C+D** | Pesos de risco iguais | | | **+1,8%/mês · Sharpe 1,31 · queda máx. −14%** |
| E | Momentum em ações da B3 | Ações líquidas | Mensal (você executa) | +15,6%/ano (2014–2026) |

Os sinais B, C e D usam 1h de atraso extra, que é o caso conservador.

**Ajustes do estudo 3:**
- O módulo B passa a usar **exposição ajustada pela volatilidade prevista**. Fora da amostra, o Sharpe subiu de 0,75 para 1,05 e a queda máxima caiu de −29% para −19%.
- A **equação de atenção e fluxo** (proximidade da máxima/mínima de 30 dias, volume anormal, fluxo agressor) roda **só em modo simulado**: rendeu +1,5%/mês fora da amostra, mas não elevou o Sharpe da carteira.

**Descartado pelos estudos:** os setups populares de day trade (MME 9/21, 9.1, VWAP, RSI, ORB, ICT etc.) e o "fade" deles, que perdem depois dos custos. Também ciclos de Fourier, entropia, curvatura, wavelets, números redondos, ímãs de liquidação, arbitragem estatística (PCA/OU, Kalman) e venda de volatilidade, que não mostraram vantagem fora da amostra.

## 2. Nível de alavancagem (decisão sua)

| Opção | Média mensal histórica (2022–2026) | Ano mediano simulado | Chance de ano no prejuízo | Chance de queda ≥ 50% | Queda máxima histórica |
|---|---|---|---|---|---|
| **1× (recomendada para começar)** | +1,9% | +22% | 11% | 0% | −14% |
| 2× | +3,8% | +43% | 14% | 0% | −27% |
| **2,8× (meta de 5%/mês)** | +5,3% | +63% | 14% | 4% | −36% |
| 5× | +9,9% | +102% | 20% | 43% | −57% |

**Importante:**
- Desde mar/2025 a combinação ficou praticamente de lado (+5% a 1×). A vantagem existe, mas está diminuindo.
- A meta de 5%/mês só aparece **na média** e com ~3× de alavancagem. A maioria dos anos simulados não a atinge.

## 3. Arquitetura (custo zero)

```
GitHub (repositório público: código, histórico, relatórios, Issues de alerta)
└─ GitHub Actions
   ├─ runner próprio no Brasil (VM "Always Free" da Oracle em São Paulo, ou seu PC)
   │   necessário porque a API da Binance bloqueia os servidores do GitHub nos EUA,
   │   e os sinais B/C/D precisam de dados em tempo quase real
   │   ├─ sinais-hora.yml   (a cada hora): lê posicionamento/OI/preço → posições-alvo B, C, D
   │   ├─ tendencia-dia.yml (00:10 UTC): módulo A
   │   └─ executor: soma as posições-alvo × alavancagem escolhida, só opera se o desvio > limite
   ├─ runners gratuitos do GitHub (EUA)
   │   ├─ acoes-mensal.yml: ranking de momentum da B3 → Telegram/Issue
   │   ├─ saude.yml: confere execução, drawdown e divergência do backtest; pausa tudo se preciso
   │   └─ reestudo.yml (mensal): reroda os estudos para detectar perda de vantagem
   └─ notificações: Telegram (bot gratuito)
```

**Proteções:**
- chave de API **sem permissão de saque**;
- alavancagem máxima fixa;
- *kill switch* por variável do repositório;
- pausa automática se a queda passar do limite definido;
- **modo simulado por 2 a 3 meses** antes do dinheiro real.

## 4. Pontos a resolver no Passo 2

1. **Corretora de perpétuos** acessível a partir do runner no Brasil. Os sinais foram estudados com dados da Binance; outra corretora exige validar que o sinal se mantém.
2. **Runner no Brasil:** criar a VM gratuita (ou usar seu computador) e registrá-la como runner do repositório.
3. **Telegram:** bot para relatórios e alertas.
4. **Capital, alavancagem (seção 2) e limite de queda** para a pausa automática.
5. **Tributação:** relatório mensal de operações para o imposto.
