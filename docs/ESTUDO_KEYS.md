# Estudo 4: dá para ganhar dinheiro com keys de jogos (G2A, Kinguin, Eneba e similares)?

> Data: 03/11/2026. Fontes externas no fim do documento; análise de dados em [`research/keys/`](../research/keys).

## Resposta curta

- **Revender keys (comprar barato e vender na G2A, Gamivo, Kinguin ou Eneba) não compensa.** Analisei 560 operações reais de um revendedor brasileiro (2021–2023). O lucro médio foi de **€0,05 por key**, com **um terço das vendas no prejuízo**. Além disso, o estoque barato quase sempre vem de fontes que violam termos de uso (keys do Humble Bundle, preço regional) ou de fraude (cartão roubado), o que leva a keys revogadas e contas banidas.
- **Quem ganha nesse mercado sem estoque nem risco** são as plataformas (taxa de 20–30% nas keys baratas) e os **comparadores de preço que vivem de afiliado** (AllKeyShop, GG.deals). É a única parte do ecossistema que cabe nas nossas regras: custo zero, 100% automatizável, sem capital e sem infringir termos.
- **Recomendação:** um comparador de preços e canal de promoções de jogos **feito para o Brasil**, monetizado por afiliados. Ele mostraria o preço final em R$ com IOF, se a key ativa no Brasil, se a loja é oficial ou marketplace, a menor marca histórica e os jogos grátis da semana.

## 1. Como o mercado funciona

| Peça | Como funciona |
|---|---|
| **Marketplaces** (G2A, Kinguin, Eneba, Gamivo, K4G, Driffle) | Terceiros anunciam keys e o marketplace cobra taxa. Juntos têm dezenas de milhões de visitas/mês (G2A ≈ 34,7 mi/mês em out/2025). |
| **Lojas oficiais** (Steam, GOG, Epic, Nuuvem, Green Man Gaming, Fanatical, Humble) | Vendem keys autorizadas pelas publicadoras. |
| **Atacado B2B** (CodesWholesale, Kinguin API, G2A Integration API) | APIs para comprar keys em lote e revender numa loja própria. A Kinguin exige saldo pré-pago, negociado com um gerente comercial, e só aceita devolução de key não resgatada em até 24h. |
| **Comparadores** (AllKeyShop, GG.deals, IsThereAnyDeal) | Mostram o menor preço entre lojas e ganham comissão de afiliado e publicidade. O GG.deals tem API de preços com chave gratuita (oficiais + keyshops, por região). |

### Taxas (o que o vendedor perde)

- **G2A:** o comprador paga, sobre o preço do vendedor, cerca de **+30%** em keys de €1 a €3,50, **+25%** de €4 a €7, **+20%** em torno de €10 e **+12–15%** acima de €20. Em 2021 chegava a **+44%** abaixo de €2,50. São números de uma tabela real de um vendedor, com datas de 2021 e 2023.
- **Eneba** (termos oficiais): 6% + €0,20–0,25 por venda.
- **Kinguin:** cerca de 11% (fonte não oficial).
- Há também cadastro empresarial (KYC), taxas de saque e de câmbio.

## 2. A economia real de um revendedor brasileiro

Encontrei no GitHub o código e as planilhas de controle de um revendedor brasileiro. O código é um robô que reprecifica automaticamente para ficar um centavo abaixo dos concorrentes. As planilhas trazem 560 operações com custo e preço, de 2021 a 2023. **As planilhas contêm dados pessoais de clientes**, então usei só números agregados e não reproduzo nem o endereço nem os dados.

| Métrica | Valor |
|---|---|
| Canais | Gamivo 244, G2A 166, Kinguin 19 vendas anunciadas |
| Keys vendidas | 284 de 560 (51%); o resto ficou encalhado |
| Preço de venda mediano | **€1,05** (34% abaixo de €1; 99% abaixo de €5) |
| Custo mediano por key | €0,42 |
| Quanto chega ao vendedor | **81%** do preço anunciado |
| **Lucro por key** | **média €0,05**, mediana €0,17; 10% piores: −€0,80 |
| Vendas com prejuízo | **33%** |
| Devoluções | 1,8% |
| Origem do estoque | keys do Humble Bundle compradas de "traders", pagas principalmente com chaves de TF2 (200 operações) e PayPal (69) |

**Leitura:**
- É um negócio de centavos: muitos bots disputam o primeiro lugar da lista e o preço desce até a margem sumir.
- Para ganhar R$ 1.000 por mês com €0,05 por key seriam necessárias cerca de **3.600 keys vendidas por mês**. Isso exige um estoque que só existe em fontes problemáticas.

## 3. Riscos de revender

1. **Origem do estoque:**
   - Os termos do Humble Bundle proíbem revender keys, que são para uso não comercial.
   - A Valve restringiu as regras de keys e presentes justamente para conter revendedores.
   - Comprar em regiões baratas para revender em regiões caras é exatamente o que as restrições regionais tentam impedir.
2. **Fraude:** boa parte das keys baratas do mercado cinza é comprada com cartão roubado. Quando o estorno acontece, a publicadora pede à Valve para revogar a key. Há casos documentados: Rebellion revogou mais de 7.000 keys de Sniper Elite 3; a tinyBuild relatou US$ 450 mil em keys desviadas; a G2A pagou US$ 40 mil à desenvolvedora de Factorio. O revendedor fica com o prejuízo e com a reputação queimada.
3. **Contas:** a Steam pode suspender contas ligadas a presentes de origem fraudulenta, e o Humble pode banir contas de revendedores.
4. **Jurídico:** não achei regra brasileira específica. Na Europa, o Tribunal de Justiça da UE (caso Tom Kabinet, 2019) não aceitou a revenda de cópias digitais como livre. É uma área cinzenta, e o risco é seu como pessoa física ou empresa.
5. **Capital e operação:** exige estoque ou saldo pré-pago, cadastro empresarial em cada marketplace, atendimento e disputa de reclamações.
6. **Nossas regras:** o GitHub Pages proíbe e-commerce. Uma loja própria exigiria hospedagem fora do GitHub.

## 4. Modelos de negócio avaliados

| Modelo | Capital | Custo de infra | Risco | Margem real | Automatizável no GitHub? | Veredito |
|---|---|---|---|---|---|---|
| **A. Revenda no mercado cinza** (bundles, trocas, preço regional) | Sim (estoque) | Zero | **Alto** (termos de uso, revogação, banimento) | ≈ €0,05/key | Parcial | ❌ Não |
| **B. Loja própria abastecida por API** (Kinguin/CodesWholesale → loja em R$ com Pix) | Sim (saldo pré-pago) | Precisa de hospedagem de e-commerce | Médio (fornecedor, atendimento, procedência) | Limitada: o cliente compara com G2A/Eneba | Não (Pages proíbe e-commerce) | ⚠️ Só numa fase futura |
| **C. Comparador e canal de promoções BR com afiliados** | **Não** | **Zero** | **Baixo** | 2–5% (até 10% em bundles) de cada venda indicada, sem estoque | **Sim** (Actions + Pages + Telegram) | ✅ **Recomendado** |

### O modelo C em números (honestos)

- **Comissões típicas de afiliado:**
  - Green Man Gaming: até 5%, ou 10% em bundles;
  - Fanatical: até 5%;
  - Eneba: ≈ 5%;
  - G2A Goldmine: 4–5%;
  - Nuuvem: ≈ 2,4% no programa EUA/Canadá; o do Brasil precisa ser confirmado.
- **Ticket médio estimado:** R$ 60, o que dá **≈ R$ 2–3 por venda**. Com conversão de 3–5% dos cliques, são **≈ R$ 100 a cada 1.000 cliques**.

| Cenário (mês 6) | Cliques/mês | Receita/mês |
|---|---|---|
| Pessimista | 1.000 | ≈ R$ 100 |
| Base | 10.000 | ≈ R$ 1.000 |
| Otimista | 50.000 | ≈ R$ 5.000 + patrocínios |

**O risco principal é audiência**, como em qualquer canal novo. A vantagem do nicho de jogos é que há "ganchos" gratuitos que fazem o canal crescer sozinho: os jogos grátis da Epic toda semana, giveaways, as grandes promoções da Steam (verão: 25/06–09/07; fim de ano: 17/12/2026–04/01/2027) e o alerta "menor preço da história".

**Diferencial para o Brasil (o que os comparadores gringos não fazem bem):**
- preço final em R$ já com IOF, comparado com o preço regional da Steam Brasil;
- aviso se a key **ativa no Brasil**, uma queixa frequente com keys "globais";
- selo de **loja oficial × marketplace** e de risco de procedência;
- formas de pagamento brasileiras (Pix).

## 5. Arquitetura sugerida para o modelo C (custo zero)

```
GitHub Actions (cron)
├─ coletar.yml (a cada 2–4h): APIs gg.deals + IsThereAnyDeal + CheapShark (chaves gratuitas)
│     → preços oficiais e de keyshops por jogo e região, histórico guardado no repositório
├─ curar.yml: regras de "boa oferta" (menor preço em 90 dias, desconto real vs média,
│     loja confiável, ativa no BR) + jogos grátis da semana
├─ publicar.yml: Telegram/Discord (bot gratuito) + site estático no GitHub Pages
│     (comparador e histórico de preços; sem vender nada: só links de afiliado)
└─ medir.yml (diário): cliques e conversões dos painéis de afiliados → prioriza o que vende
```

Os runners do GitHub têm internet aberta, então as APIs de preço funcionam lá, embora estejam bloqueadas no ambiente desta sessão. O site é de conteúdo e comparação, sem transações, o que é compatível com as regras do GitHub Pages.

## 6. Onde estamos depois de 4 estudos

| Caminho | Precisa de capital? | Retorno robusto encontrado | Risco |
|---|---|---|---|
| Trading (estudos 1–3) | Sim | ≈ 1,5–2% ao mês sobre o capital, sem alavancagem | Perda de capital; vantagem enfraquecendo desde 2025 |
| Revenda de keys (este estudo) | Sim | ≈ €0,05 por key | Alto (termos de uso, fraude) |
| **Afiliados em nicho com audiência** (proposta 1 e este modelo C) | **Não** | Proporcional à audiência: ≈ R$ 100 por 1.000 cliques | Baixo; o desafio é crescer o público |

**Sem capital, o caminho realista é o afiliado com audiência.** Com capital, o trading entra como complemento.

## Fontes

- Taxas e API da G2A: [G2A (taxa única)](https://www.g2a.co/g2a-com-streamlines-the-commission-fees-structure-for-sellers/), [ChannelX](https://channelx.world/2020/11/turn-your-passion-for-gaming-into-business-with-g2a-com/); taxas da Eneba: [termos oficiais](https://eneba.com/vendor-fee-and-commission-terms-and-conditions); API da Kinguin: [kinguinltdhk/Kinguin-eCommerce-API](https://github.com/kinguinltdhk/Kinguin-eCommerce-API); API da G2A: [g2a-official/integration-api-client](https://github.com/g2a-official/integration-api-client); atacado: [CodesWholesale](https://codeswholesale.com/)
- Revogação, fraude e casos: [MCV/tinyBuild](https://www.mcvuk.com/tinybuild-we-lost-450000-in-revenue-to-grey-market-key-sellers/), [PC Gamer/Rebellion](https://www.pcgamer.com/au/rebellion-revokes-unlicensed-sniper-elite-3-keys-offers-free-target-hitler-dlc-as-compensation), [TechSpot/Factorio](https://www.techspot.com/community/topics/g2a-agrees-to-pay-factorio-dev-40-000-for-selling-stolen-game-keys.262819/), [PC Gamer/esquema brasileiro](https://pcgamer.com/au/a-brazilian-hacker-explains-how-g2a-game-key-scams-work), [TecMundo](https://www.tecmundo.com.br/voxel/180324-g2a-admite-ter-vendido-chaves-fraudadas-de-jogos-da-plataforma.htm), [bugnet.io](https://bugnet.io/blog/how-key-reseller-sites-affect-indie-devs), [Naavik](https://naavik.co/podcast/inside-the-pc-game-gray-market-economy/)
- Regras da Valve e do Humble: [Xsolla](https://xsolla.com/blog/exploring-valves-revised-rules-for-steam-keys), [KitGuru](https://www.kitguru.net/gaming/matthew-wilson/valve-updates-steam-gift-rules-to-limit-key-resellers/), [CyberPost](https://cyberpost.co/?p=1290170), [Game Informer/Humble](https://gameinformer.com/b/news/archive/2014/03/29/7-entertainment-updates-terms-to-prohibit-the-resale-of-humble-bundle-keys.aspx), [SteamGifts](https://www.steamgifts.com/discussion/1zvi8/humble-bundle-disabling-accounts)
- Afiliados: [G2A Goldmine](https://www.g2a.co/cooperation/refferal-and-partner-program/), [Awin/G2A](https://www.awin.com/us/news-and-events/program-news/new-affiliate-program-g2a), [Eneba (Lasso)](https://getlasso.co/affiliate/eneba-com/), [Green Man Gaming](https://www.greenmangaming.com/es/affiliates/), [Fanatical](https://uppromote.com/affiliate-program-directory/fanatical), [Nuuvem (FlexOffers)](https://www.flexoffers.com/affiliate-programs/nuuvem-us-ca/)
- Comparadores e APIs: [gg.deals Prices API](https://gg.deals/api/prices/), [IsThereAnyDeal docs](https://docs.isthereanydeal.com/), [Tested.gg/AllKeyShop](https://tested-9hz.pages.dev/site/allkeyshop), [Kustiq/AllKeyShop](https://kustiq.com/company/allkeyshop.com)
- Mercado e Brasil: [Accio/G2A](https://www.accio.com/business/g2a), [ECDB/Kinguin](https://ecdb.com/resources/sample-data/retailer/kinguin), [Ahrefs/Kinguin](https://ahrefs.com/websites/kinguin.net), [Steam (ativação no BR)](https://steamcommunity.com/discussions/forum/27/4202490424041452020), [Canaltech (calendário Steam 2026)](https://canaltech.com.br/games/quais-sao-as-datas-de-promocao-no-steam-em-2026/), [Tecnoblog (avisos de jogos grátis)](https://tecnoblog.net/comunidade/t/avisos-de-jogos-gratis-nas-lojas/1441.md)
