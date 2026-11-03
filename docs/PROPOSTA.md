# Passo 1: Proposta técnica e de negócio

> Status: **aguardando aprovação do operador**. Nenhum código de integração foi escrito.
> Data: 03/11/2026

## 1. Decisão

**Projeto "Radar": motor autônomo de ofertas verificadas por histórico de preço, monetizado por comissão de afiliado no mercado brasileiro.**

A cada 2 horas o sistema:

1. coleta preços nas APIs de afiliados da Shopee e do AliExpress;
2. grava o histórico de cada produto no próprio repositório;
3. só considera promoção o produto cujo preço atual está **abaixo da mediana dos últimos 30 dias**;
4. publica as melhores ofertas com link de afiliado num canal do Telegram, em até 3 redes sociais (via Buffer) e num site estático com gráfico de histórico de preço.

A proposta de valor é o filtro contra o desconto falso ("metade do dobro"): em vez de repetir o preço "de/por" informado pelo vendedor, o Radar compara com o preço que ele próprio registrou. Isso se traduz em conteúdo útil e em posts que o público tende a compartilhar ("⚠️ este produto subiu 40% nas últimas 2 semanas").

### Por que agora

A Black Friday 2026 é em **27/11** (daqui a 24 dias). A projeção é de R$ 13,3 bi a R$ 16,6 bi no e-commerce na semana. A maquiagem de preço acontece justamente nas semanas anteriores. Se o coletor entrar no ar nos próximos dias, chegaremos à Black Friday com cerca de 3 semanas de histórico, o suficiente para flagrar essas altas.

## 2. Ideias avaliadas e descartadas

| Ideia | Motivo da exclusão |
|---|---|
| Blog/SEO com IA + AdSense | O AdSense não aprova subdomínio `github.io`, e domínio próprio tem custo. A política de *scaled content abuse* do Google penaliza conteúdo de IA em massa. |
| Micro-SaaS ou API paga | Exige servidor. O GitHub Pages proíbe SaaS comercial, e o Actions não é backend. |
| Produtos digitais gerados por IA (Gumroad/Etsy) | O Etsy cobra taxa por anúncio, o Gumroad não tem API de criação de produto, e o mercado está saturado. |
| Canal "faceless" de vídeo IA (YouTube/TikTok) | A monetização exige o YPP (1 mil inscritos + 10 mi de views em Shorts em 90 dias). Há política contra conteúdo inautêntico, e uploads via API não auditada ficam privados. |
| Trading ou cripto | Exige capital e tem risco de perda. Mineração é proibida no Actions. |
| Newsletter automatizada | A receita depende de base grande, e as APIs de publicação (Beehiiv etc.) são pagas. |
| **Ofertas verificadas + afiliados (escolhida)** | O modelo já funciona no Brasil (canais de promoção no Telegram), as APIs de afiliado são gratuitas, o conteúdo é baseado em dados reais (não é spam de IA) e não exige servidor nem domínio. |

## 3. Modelo de negócio

- **Receita:** comissão por venda (CPS). Shopee: comissão variável por categoria, mais comissão extra de vendedores. AliExpress: cerca de 3% a 9%. O cookie costuma comissionar o carrinho inteiro, não só o item clicado.
- **Custo:** R$ 0 (detalhes na seção 6).
- **Recebimento:** as plataformas validam o pedido antes de pagar, então o primeiro dinheiro entra em cerca de **45 a 75 dias**.
- **Fases futuras:** Amazon BR (o acesso à API exige vendas prévias) e Mercado Livre (sem API pública de link de afiliado; a geração é manual no painel).

### Projeção honesta (mês 3)

Premissas: ticket médio de R$ 90, comissão efetiva de 5% (≈ R$ 4,50 por pedido) e conversão de clique em pedido de 3%. Isso dá ≈ **R$ 135 por 1.000 cliques**.

| Cenário | Cliques/mês | Pedidos | Receita/mês |
|---|---|---|---|
| Pessimista (o canal não decola) | 300 | 9 | ~R$ 40 |
| Base | 3.000 | 90 | ~R$ 400 |
| Otimista | 15.000 | 450 | ~R$ 2.000 |

Na semana da Black Friday, ticket e conversão sobem bastante. O teto escala horizontalmente: cada nicho novo (ex.: "Radar Tech", "Radar Casa") é só um arquivo de configuração a mais, com o mesmo custo zero.

**Risco principal:** audiência. O sistema automatiza 100% da oferta, da curadoria e da publicação. O crescimento do público, porém, é orgânico (compartilhamento, Pinterest, SEO de cauda longa) e é a maior incerteza do projeto. Recomendo uma divulgação inicial opcional de cerca de 30 minutos feita por você, uma única vez. Depois disso, tudo roda sozinho.

## 4. Arquitetura técnica

```
                    GitHub Actions (repo público → minutos ilimitados)
┌──────────────────────────────────────────────────────────────────────────┐
│ pipeline.yml  (cron a cada 2h, ~3 min)                                   │
│                                                                          │
│  [1] COLETA         Shopee Affiliate GraphQL ─┐                          │
│      (adaptadores)  AliExpress Affiliate API ─┴─► produtos normalizados  │
│                                                                          │
│  [2] HISTÓRICO      grava só MUDANÇAS de preço (JSONL mensal)            │
│                     no branch `data` (git como banco de dados)           │
│                                                                          │
│  [3] PONTUAÇÃO      desconto real vs mediana 30d, vendas, nota,          │
│                     comissão esperada, peso da categoria (bandit),       │
│                     penalidade de repetição                              │
│                                                                          │
│  [4] ENRIQUECIMENTO Gemini (lotes de ~40 itens/chamada, saída JSON):     │
│                     título limpo, frase curta, categoria                 │
│                     fallback: modelo flash-lite → Gemma → template fixo  │
│                                                                          │
│  [5] MÍDIA          card PNG gerado com Pillow (foto, preço, selo        │
│                     "menor preço em 30 dias")                            │
│                                                                          │
│  [6] PUBLICAÇÃO     Telegram Bot API → canal (conversão principal)       │
│                     Buffer GraphQL   → até 3 redes (Pinterest/Threads/…) │
│                     Site estático    → GitHub Pages (histórico + RSS)    │
└──────────────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────────────────┐
│ metrics.yml (diário)   relatórios de conversão Shopee/AliExpress         │
│                        → atualiza pesos por categoria e horário          │
│                          (Thompson sampling: aprende o que vende)        │
│ health.yml  (diário)   checa se o cron rodou, quotas e erros de API;     │
│                        abre Issue no repo se algo quebrar                │
│ maintenance.yml (sem.) compacta histórico, remove produtos mortos,       │
│                        mantém o repo < 1 GB                              │
└──────────────────────────────────────────────────────────────────────────┘
```

### Stack (tudo open-source)

Python 3.12, `httpx`, `pydantic`, `jinja2`, `Pillow` e `pytest`. Não há servidor nem banco de dados externo: o próprio git guarda o histórico. Os gráficos do site são SVG inline, sem bibliotecas JavaScript.

### Pontuação da oferta (resumo)

```
score = desconto_real × w1 + log(vendas) × w2 + nota × w3
      + comissão_esperada × w4 + peso_categoria(bandit) × w5
      − penalidade(publicado nos últimos 7 dias)

desconto_real = 1 − preço_atual / mediana_30d
  (só calculado com ≥ 5 leituras em ≥ 3 dias;
   antes disso o item recebe o selo "novo no radar")
```

### Site estático (GitHub Pages)

- **Home:** as melhores ofertas do momento.
- **`/p/<id>`:** gráfico de histórico, menores preços em 30/60/90 dias e botão de afiliado com `rel="sponsored nofollow"`.
- **Categorias, `feed.xml` e `sitemap.xml`:** dão SEO de cauda longa para buscas como "histórico de preço de X".
- **Dataset aberto (CSV):** reforça o caráter de projeto de transparência de preços.

### Orçamento de uso diário

| Recurso | Uso previsto | Limite gratuito |
|---|---|---|
| GitHub Actions | ~12 execuções × ~3 min | Ilimitado em repo público |
| Gemini | ≤ 12 chamadas (em lote) | Varia por modelo (≈ 20 a 1.000+ RPD) |
| Telegram Bot API | ~15 a 25 posts | Gratuito (30 msg/s) |
| Buffer | ~3 a 5 posts por canal, fila ≤ 10 | 3 canais, 10 posts na fila por canal |
| GitHub Pages | site < 200 MB | 1 GB de site, ~100 GB/mês de banda |

Verifiquei os modelos disponíveis na chave Gemini conectada a esta sessão: há `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemma-4-31b-it` e outros. O desenho funciona mesmo no pior cenário de quota (20 RPD), porque agrupa ~40 itens por chamada e tem fallback para template fixo. O Replicate **não será usado**: é pago por uso, o que viola a regra de custo zero.

## 5. Conformidade e riscos

| Risco | Mitigação |
|---|---|
| **Termos do GitHub Pages** proíbem sites "primariamente voltados a transações comerciais" | O site não transaciona: é um projeto de histórico de preços e dados abertos com links externos identificados. O build é portátil e migra para o Cloudflare Pages (grátis, via CLI `wrangler`) sem mudar código. Risco moderado, que declaro abertamente. |
| **Termos do Actions:** uso deve estar ligado a construir e publicar o projeto do repo | Os workflows constroem e publicam o site e o dataset deste próprio repositório. Os jobs são curtos e leves. |
| Cron desativado após 60 dias sem atividade no repo | Cada execução faz commit de dados, e o `health.yml` abre uma Issue se o cron parar. |
| Aprovação de afiliado demora dias; a API "Advanced" do AliExpress exige pedido separado | As fontes são plugáveis: o sistema começa com a que for aprovada primeiro. |
| Quotas do Gemini mudam sem aviso | Chamadas em lote, cadeia de fallback e template determinístico: a publicação nunca para por falta de IA. |
| API do Buffer em beta pública, com mudanças incompatíveis | Fica isolada num adaptador. O Telegram é o canal principal e independe do Buffer. |
| Publicidade (CONAR/CDC) e termos dos programas de afiliado | Todo post traz identificação de link de afiliado e a hora do preço verificado ("preço pode mudar"). Sem spam, sem urgência falsa e sem compra de palavra-chave de marca. |
| Audiência (cold start) | Posts de alerta compartilháveis, Pinterest (tráfego de longo prazo), SEO e divulgação inicial opcional. |

## 6. Custo total

**R$ 0/mês.** Repo público (Actions ilimitado), GitHub Pages, Telegram, Buffer Free, Gemini free tier e programas de afiliado gratuitos. Nenhum domínio, servidor ou cartão de crédito é necessário.

## 7. Cronograma

| Quando | O quê |
|---|---|
| Hoje | Aprovação desta proposta |
| D0–D1 | **Passo 2:** lista detalhada de contas e chaves. Os cadastros de afiliado devem começar já, pois a aprovação leva dias. |
| D1–D3 | **Passo 3:** MVP com coleta, histórico, Telegram e site |
| D3–D24 | Histórico acumulando, Buffer, métricas e otimização automática |
| **27/11** | Black Friday com o detector de desconto falso no ar |

## Fontes

- Black Friday 2026: [Meio & Mensagem](https://www.meioemensagem.com.br/marketing/black-friday-deve-movimentar-r-133-bi-no-e-commerce), [GiroNews (Abiacom)](https://gironews.com/varejo-digital/black-friday-deve-movimentar-r-166-bilhoes-no-e-commerce-brasileiro-em-2026/), [Omie](https://www.omie.com.br/blog/black-friday-2026-e-commerce-faturamento/)
- Shopee Affiliate Open API (BR): [shopee-affiliate (GitHub)](https://github.com/gregojoao/shopee-affiliate), [Shopee.Affiliate (NuGet)](https://www.nuget.org/packages/Shopee.Affiliate), [Apify: Shopee Affiliate Products](https://apify.com/viralanalyzer/shopee-affiliate-products)
- AliExpress Affiliate API: [Zuplo: guia da API AliExpress](https://zuplo.com/blog/2024/10/02/aliexpress-api-guide), [Botize: AliExpress Affiliates](https://botize.com/en/app/aliexpress_associates)
- Mercado Livre (sem API de link): [Divulga Ninja](https://www.divulganinja.com.br/blog/como-gerar-link-afiliado-mercado-livre-passo-a-passo-2026), [Mercado Livre Afiliados](https://mercadolivre.com.br/l/afiliados-home)
- Buffer API: [Buffer: API aberta](https://buffer.com/resources/buffer-api-is-here/), [Buffer for Developers](https://buffer.com/made-for/developers), [API Report Card](https://supergood.ai/api-report-card/buffer)
- Gemini free tier: [ScriptByAI](https://www.scriptbyai.com/gemini-api-free-tier-limits/), [YingTu](https://yingtu.ai/en/blog/google-gemini-api-free-tier-limits-2026)
- GitHub: [Limites do GitHub Pages](https://docs.github.com/en/enterprise-server@3.22/pages/getting-started-with-github-pages/github-pages-limits), [Desativar/ativar workflows (regra dos 60 dias)](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)
