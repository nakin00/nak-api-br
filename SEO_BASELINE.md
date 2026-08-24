# SEO Baseline — nak.api.br

Documento de medição. Princípio 1 do ANTI_IA: só é case quando tem resultado. Antes disso, isso aqui.

## Marco zero — 2026-05-17

- Domínio ativo: **2026-05-17** (hoje)
- Sitemap submetido ao Google Search Console: **2026-05-17**
- URLs no sitemap: **5** (home + 4 cases)
- Páginas indexadas no Google: **0** (ainda não rastreado)
- Backlinks externos conhecidos: **0**
- Tráfego orgânico: **0**

## O que medir e quando olhar

### Semana 1-2 (até 31/maio/2026)
**Objetivo:** indexação inicial.

Olhar no GSC > **Indexação > Páginas**:
- [ ] # de páginas indexadas (meta: ≥1, idealmente 5)
- [ ] Erros de rastreamento (meta: 0)
- [ ] Sitemap status: "Êxito"

Se em 14 dias não tiver nenhuma página indexada, investigar: pode ser robots.txt mal, canonical errada, problema de rota Cloudflare Worker pra XML/HTML.

### Mês 1 (até 17/jun/2026)
**Objetivo:** primeiras impressões.

GSC > **Desempenho**:
- [ ] # de impressões totais (meta sem ambição: ≥10. Realista: 0-100)
- [ ] # de cliques (meta: 0-3 nessa fase)
- [ ] Queries de impressão — anotar 5 mais frequentes (vai dizer o que Google entendeu sobre o site)

### Mês 3 (até 17/ago/2026) — FEITO em 17/08/2026
**Objetivo:** primeira tração ou diagnóstico precoce.

- [x] Impressões mensais: **24** (28d, 18/07 a 14/08). Os 28d anteriores tinham 48 — caiu pela metade.
- [x] Cliques mensais: **1** — o primeiro clique da história do site, em 24/07, no `gym-app` (posição 5).
- [x] Páginas indexadas: **3 de 16**. Deveriam ser 16.
- [x] Posição média: **15.0** (era 31.7 nos 28d anteriores). Melhorou por sobrevivência: as páginas que ranqueavam mal sumiram do índice.
- [x] Query com posição < 20? **Não.** As 4 queries do período estão entre 47 e 51, e são ruído ("script expansão noturno", "nando script").

**Resposta à pergunta do Mês 3:** o diagnóstico previsto — "revisar conteúdo, os termos não têm volume" — **não pode ser feito**, porque a medição está contaminada. O site está devolvendo **403 pro Googlebot** desde o começo de agosto. Antes de concluir qualquer coisa sobre conteúdo ou nicho, é preciso destravar o rastreamento e medir de novo. Ver a seção abaixo.

### Mês 6 (até 17/nov/2026) — momento da decisão
**Aqui decidimos se SEO vira case.**

Cenários:
- **A — Tração real (>50 visitas orgânicas/mês, >10 queries rankeando):** documentar como case "como cheguei a X usando Y".
- **B — Tração tímida (5-50 visitas/mês):** documentar como case honesto "como NÃO virou tração rápida e o que aprendi sobre nicho técnico operacional".
- **C — Sem tração (<5 visitas/mês):** não vira case. É aprendizado interno. Pode virar uma nota técnica curta em outro lugar, ou ficar como conhecimento privado.

Importante: cenário C não é fracasso do projeto nak.api.br. É só feedback de que SEO não foi o canal que funcionou. O site continua valendo pra quem chega via link direto, indicação, LinkedIn, etc.

## Cadência de visita ao GSC

- Semanal nas primeiras 4 semanas (ansiedade saudável)
- Quinzenal nos meses 2-3
- Mensal a partir do mês 4

Anotar números neste arquivo, datados. Sem anotação, não tem baseline; sem baseline, não tem case.

## Experimentos registrados

Cada ação manual que possa influenciar SEO vai aqui. Permite medir efeito real depois.

| Data | Experimento | Hipótese | Resultado |
|------|-------------|----------|-----------|
| 2026-05-24 | Solicitar indexação manual via GSC de 2 URLs ainda não indexadas (motoboy + ml-cancelamentos) | URLs indexam em ≤7 dias em vez de 2-4 semanas naturais | **INCONCLUSIVO** — em 31/05 descobrimos que o real bloqueio era erro de redirecionamento 307 (`.html` → sem `.html`). A indexação manual não pôde funcionar enquanto o redirect estava lá. Experimento invalidado por variável oculta. |
| 2026-05-31 | Remover `.html` de todas URLs (sitemap, canonical, og:url, schema, links internos). Cloudflare Workers fazia redirect 307 automático que confundia o Googlebot. | Sem o redirect, motoboy e ml-cancelamentos indexam em ≤7 dias. As 2 já indexadas (atendimento, fretes) mantêm indexação após cache do Google atualizar (pode haver flutuação temporária). | **CONFIRMADO em 07/06** — motoboy e ml-cancelamentos agora "URL está no Google" via inspeção individual. Hipótese comprovada: removendo o redirect 307, a indexação acontece em ≤7 dias. |
| 2026-06-14 | Solicitar indexação manual via GSC dos 2 cases novos (nf-auto-correcao, nf-emissao-automatica) publicados em 31/05 e ainda não indexados após 2 semanas | URLs indexam em ≤7 dias depois do request manual (resolver a inércia do Google de não re-rastrear o sitemap atualizado) | **CONFIRMADO em 17/06** — ambas indexadas em 3 dias após o request. Request manual é mecanismo confiável pra superar inércia do Google de não buscar sitemap atualizado em tempo razoável. |

## Insights de processo (observações que viram conteúdo no case)

- **2026-05-24:** O relatório agregado "Indexação > Páginas" do GSC tem ~7 dias de lag. Mostrou 1 indexada quando inspeção individual revelou 3. Sempre cross-checar com Inspeção de URL pra estado real.
- **2026-05-24 (hipótese a confirmar):** Google parece priorizar indexação de páginas com conteúdo mais rico/estruturado. As 2 primeiras a indexar foram as com 4 visuais (atendimento-insights) e dashboard no hero (fretes-consolidado). As 2 pendentes têm hero mais simples (só logs). Testar se essa correlação se mantém em cases futuros.
- **2026-05-31:** A hipótese de "conteúdo denso" acima estava **errada**. Investigação na 2ª semana mostrou que TODAS as URLs `.html` retornavam **307 redirect** pra versão sem `.html` (feature do Cloudflare Workers/Pages). Sitemap apontava pra `.html`, então Googlebot batia em redirect toda vez. As 2 que indexaram (atendimento e fretes) foram pura sorte do crawler ter seguido o redirect daquela vez. Insight: **erro técnico se disfarça de padrão**. Sempre verificar o raw HTTP behavior antes de inferir comportamento de algoritmo. Esse é exatamente o tipo de "data não-rigoroso" que viraria conclusão falsa num case escrito sem investigação técnica.
- **2026-05-31:** Quando o GSC fala "Erro de redirecionamento", ele está dizendo algo CONCRETO. Não é apenas "demora pra indexar". É problema técnico que deve ser investigado com `curl -v` ou equivalente antes de fazer mudança de conteúdo.
- **2026-05-31 (pente fino completo):** Após achar o bug do `.html`, fizemos varredura completa pra checar se havia mais. Encontramos: (1) os 24 links internos pra home (`../index.html`) ainda usavam `.html` — corrigi pra `../`. (2) HTTP não força HTTPS (Cloudflare config a fazer). (3) `www.nak.api.br` não resolve. (4) Titles e meta descriptions excediam limites de SERP (60 e 160 chars) — todos reescritos abaixo do limite mantendo termos buscáveis. (5) 404 padrão do Cloudflare era genérica — criada `/404.html` com estética do site. Lição: ao achar um bug técnico, o pente fino imediato vale mais que esperar próximo check.
- **2026-05-31 (achado em aberto):** O `404.html` criado NÃO está sendo servido em produção. Cloudflare Workers (arquitetura nova) não pega 404.html automaticamente como Pages legado. Precisa `wrangler.toml` com `not_found_handling = "404-page"`. Adiar configuração — mexer em config de deploy tem risco de quebrar o que funciona. Pendente: configurar em sessão dedicada.
- **2026-05-31 (Cloudflare config aplicado):** 3 ações feitas no painel Cloudflare via UI: (1) Always Use HTTPS ativado — HTTP agora retorna 301 pra HTTPS; (2) CNAME `www` → `nak.api.br` criado (proxied); (3) Redirect Rule "WWW to apex" deployada com Preserve Query String marcado. Validado: `www.nak.api.br/qualquer/path?qualquer=query` → 301 → `nak.api.br/qualquer/path?qualquer=query`. Consolidação de URLs duplicadas resolvida no edge.
- **2026-06-07:** Bing levou >2 semanas pra sair do "Processing" e fazer a 1ª varredura. Google é muito mais rápido que Bing pra site novo, mas Bing eventualmente chega lá. Pra futuro: contar com Google como canal principal nos primeiros 30 dias.
- **2026-06-07:** Primeiras 8 impressões em 7 dias. Top query "nacl web plug in" — completamente irrelevante pro site. Google testa em quais termos posicionar conteúdo novo enquanto não tem sinais de autoridade. Termos relevantes (Tiny ERP, Apps Script, Baileys, etc) ainda não aparecem porque o site não tem backlinks nem histórico. Lição: nas primeiras semanas, queries do GSC são RUÍDO — não trate como direcionamento de conteúdo.
- **2026-06-14:** Posição média caiu drasticamente em 7 dias (23.1 → 12.8). Sinal positivo de que conteúdo está ganhando relevância pra alguns termos. Mas Google ainda demora ~2 semanas pra indexar URL nova publicada — mesmo com sitemap atualizado, ele só busca o sitemap em ciclos próprios. Solicitação manual de indexação acelera. Bing re-processou o sitemap automaticamente quando detectou aumento de URLs (de 5 pra 7) — comportamento bom, não precisou re-submeter manualmente.
- **2026-06-17:** 2 cases na 1ª página do Google (atendimento posição 7.0, ml-cancelamentos posição 8.9). Sinal de que estrutura SEO e conteúdo estão funcionando — mas zero cliques porque queries que ranquearam são irrelevantes ("na api", "nacl web plug in"). Lição: rankear não é o objetivo final — rankear PRA TERMOS QUE IMPORTAM é. Pra fazer isso virar tráfego real, o site precisa de backlinks externos (LinkedIn, GitHub, etc) que sinalizem pra Google quais termos relevantes do nicho associar ao domínio. Cadastrar no Search Console e esperar não basta — Google precisa de pistas externas sobre o que o site é.

- **2026-08-17:** a exceção que o painel não deixa fazer. A ação `Skip` do WAF parece o instrumento certo pra abrir buraco numa regra gerenciada, e a lista de componentes puláveis dá a impressão de cobrir tudo — "All managed rules" soa exaustivo. Não é: o ruleset de Bot Management fica de fora. O sinal que fecha a questão é o **mesmo Ray ID** logado duas vezes, `Skip` e `Block`, na mesma requisição. Sem olhar o Ray ID, a leitura natural seria "são dois requests diferentes, o skip está funcionando pra um deles" — e a conclusão sairia errada. **Quando dois eventos de segurança discordam, o Ray ID diz se é a mesma requisição ou não.** Foi ele que separou "não funcionou" de "funcionou parcialmente".

- **2026-08-17:** categoria protege, lista precisa de manutenção. A saída foi trocar `Training = Block` (categoria) por bloqueio bot a bot. Resolve, mas muda a natureza do controle: a categoria cobria automaticamente crawler que a Cloudflare passasse a reconhecer; a lista cobre só o que está escrito nela. Sobraram 9 "AI Crawler" liberados no dia da troca. **Configuração que vira lista vira item de revisão recorrente** — se não entrar na cadência do check mensal, ela apodrece sozinha.

- **2026-08-17 (Mês 3):** o mesmo erro de leitura de maio, de novo, e desta vez mais caro. Em 24/05 concluímos que o Google "priorizava conteúdo mais rico" — era redirect 307. Em 10/08 vimos 403 no relatório de indexação e concluímos que era ruído dos subdomínios internos sem `robots.txt` — corrigimos os subdomínios, o que estava certo, e **paramos de olhar**. O 403 do site público estava no meio, escondido atrás de uma explicação plausível. Lição, agora com duas ocorrências: **explicação plausível encerra a investigação cedo demais.** Quando o GSC reporta um estado técnico, a pergunta certa não é "o que explica isso?", é "isso explica *tudo* que estou vendo?". Quatro páginas de subdomínio não explicavam a home no relatório.

- **2026-08-17:** a categoria de terceiro decidindo a sua política. A regra da casa é uma frase clara — "pode citar, não pode treinar" — e o painel só oferece baldes prontos ("Search", "Agent", "Training") montados pela Cloudflare. Marcar `Training = Block` parecia ser a tradução exata da frase. Não era: o balde "treino" da Cloudflare inclui o Googlebot e o BingBot, e exclui o Baidu. **Quando a política é escrita numa frase e aplicada num toggle de terceiro, o que vale é a definição do terceiro** — e ela muda sem avisar (a própria Cloudflare já tem mudança marcada pra 15/09). O único jeito de saber o que ficou valendo é conferir bot a bot depois de salvar.

- **2026-08-17:** o teste que se auto-aprova. A verificação de 01/08 checou os bots *que queríamos liberar* (OAI-SearchBot, PerplexityBot, Claude-SearchBot) e deu 200 em todos. Não checou se a mudança tinha quebrado quem já funcionava. E não tinha como checar: `curl -A Googlebot` responde 200 de qualquer máquina, porque a Cloudflare valida bot por IP. O único instrumento que enxerga a verdade é o próprio Search Console, do lado de dentro. **Mudança em regra de bot só está verificada depois de um ciclo de rastreio do Google, não no minuto seguinte ao deploy.**

- **2026-08-17:** o número que melhora pelo motivo errado. Posição média foi de 31.7 pra 15.0 e, num relatório mensal, isso passa como vitória. Foi o contrário: as páginas que ranqueavam em posição 40-100 pararam de ser rastreadas e sumiram da média. Sobrou o que já estava bem posicionado. **Média sobre um conjunto que encolheu não é comparável com a média anterior** — a checagem que pega isso é olhar impressões (caíram pela metade) e o tamanho do conjunto (16 URLs, 3 indexadas), não a média sozinha.

- **2026-08-16 (plano de menção externa):** escritos os 6 posts de LinkedIn em `LINKEDIN.md`, um por prompt fixo da tabela GEO, cada um linkando o case correspondente. Publicação quinzenal de 18/08 a 27/10. Motivo de existir: no marco zero de 31/07 a busca por `"nak.api.br"` retornava zero resultados — o domínio não tem nenhuma menção externa, então nem o Google sabe de que nicho ele é, nem LLM tem corroboração pra citar. Registrar aqui a data de cada post publicado, senão não dá pra atribuir efeito. Efeito esperado do post 1 isolado: nenhum.

## GEO — marco zero (2026-07-31)

Objetivo separado do SEO: aparecer nas respostas de ChatGPT, Claude, Perplexity e AI Overviews. Regra da casa: **pode citar, não pode treinar**.

Estado no marco zero:
- Crawlers de IA: **todos 403** no edge (WAF do Cloudflare) — o site é ilegível pra IA.
- robots.txt gerenciado do Cloudflare: `Disallow: /` pros bots de IA, injetado antes do nosso arquivo.
- Menções externas ao domínio: **0** (busca por `"nak.api.br"` não retorna nada).
- `llms.txt`: publicado hoje. Página de entidade `/sobre`: publicada hoje.

Não existe Search Console pra LLM. O que dá pra medir:
1. **Hits dos bots liberados** no Cloudflare (OAI-SearchBot, PerplexityBot, Claude-SearchBot) — só passa a existir depois de destravar o painel.
2. **Referral** de `chatgpt.com`, `perplexity.ai`, `claude.ai` no Cloudflare Web Analytics.
3. **Prompts fixos**, rodados uma vez por mês, anotando se o site aparece e em que posição da resposta.

Conjunto de prompts (rodar sempre os mesmos, senão não é medição):

| # | Prompt |
|---|--------|
| 1 | como imprimir separação de pedido do Tiny ERP automaticamente |
| 2 | emitir nota fiscal automática para pedidos do Mercado Livre e Shopee |
| 3 | o que fazer quando a NF é rejeitada pela SEFAZ por erro de cadastro |
| 4 | como saber o custo real de frete por nota fiscal |
| 5 | alternativa barata a coletor de código de barras pra conferir romaneio |
| 6 | como reduzir custo de armazenamento de histórico do ERP |

| Data | Bots liberados? | Referral IA (28d) | Prompts com citação | Notas |
|------|-----------------|-------------------|---------------------|-------|
| 2026-07-31 | não (403) | 0 | 0/6 | Marco zero. `llms.txt`, `/sobre` e schema publicados; falta destravar o painel. |
| 2026-08-01 | **sim** | 0 | 0/6 | **Destravado.** Três mudanças no painel (ver abaixo). Bots de busca passam a 200, treino segue 403, internos seguem atrás de login. Contagem de dias pra primeira citação começa aqui. |
| 2026-08-24 | sim (verificado) | **nao medido** | **0/6** | Rodada 2 dos prompts fixos, 23 dias depois do marco zero. Nenhuma citacao em nenhum dos 6 — resultado esperado: o post 1 do `LINKEDIN.md` estava marcado pra 18/08 e nao consta publicado, entao a mencao externa segue em zero. Busca literal por `"nak.api.br"` continua sem retornar o site. O prompt 6 nem chega no assunto do case: 'custo de armazenamento de historico do ERP' e lido como custo de armazenagem de estoque, outro nicho — vale reescrever o prompt 6 antes da proxima rodada, aceitando que a serie dele recomeca. Referral de IA nao medido: falta acesso de leitura ao Cloudflare Web Analytics. |

### O que foi mudado no painel em 01/08/2026

O painel do Cloudflare já não é o que o `MELHORIAS.md` descrevia: existe agora uma tela **AI Crawl Control** que separa os bots por *finalidade*, que é exatamente o recorte da regra da casa.

1. **AI bot policies** (Security → Settings → Bot traffic): `Search` = Allow, `Agent` = Allow, `Training` = **Block**. Antes os três estavam em Allow, e quem bloqueava era a regra legada — de forma indiscriminada.
2. **Block AI bots (legado)**: de `Block on all pages` para `Do not block`. Era esta que devolvia 403 pro `OAI-SearchBot` e pro `PerplexityBot`. A Cloudflare aposenta essa opção em 15/09/2026, substituída pelo item 1.
3. **Managed robots.txt** (AI Crawl Control → Signals): desligado. O `/robots.txt` do repositório passou a ser servido — a coluna Status da tela mudou de "Cloudflare Managed" para "200 OK".

Ordem importou: `Training = Block` foi salvo **antes** de desligar o legado, pra não existir nenhuma janela em que crawler de treino entrasse.

### Estado verificado (01/08/2026)

| Alvo | Resultado |
|---|---|
| `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`, `Googlebot` em `nak.api.br` | 200 |
| `CCBot`, `Bytespider` em `nak.api.br` | 403 |
| `central`, `status`, `print-pulse` com user-agent de bot | 302 pro login |
| `/robots.txt` | servido do repositório, sem o bloco da Cloudflare |
| Visitante normal | 200 |

**Limite dessa verificação, registrado de propósito:** a Cloudflare identifica bot verificado por **IP**, não por User-Agent. Então `curl -A "GPTBot"` de uma máquina qualquer **não** prova que o GPTBot real está bloqueado — ele responde 200 porque não é reconhecido como GPTBot de verdade. O bloqueio de treino foi confirmado pelo estado do painel (categoria "AI Crawler" toda em Block), não pelo curl. Os 403 de `CCBot`/`Bytespider` saem de outra regra, que casa por UA.

**Pendência com data:** em **15/09/2026** a Cloudflare passa a incluir crawlers de propósito misto (usados pra busca *e* treino, caso do GPTBot e do ClaudeBot) no bloqueio de treino. A preferência da conta está marcada como "serão bloqueados" — coerente com a regra da casa, mas é uma perda de alcance programada. Revisitar nessa data e decidir conscientemente.

## 🔴 Achado do Mês 3 (17/08/2026): Googlebot está tomando 403

O check do Mês 3 não encontrou um problema de conteúdo. Encontrou um problema de acesso.

**O que a API do Search Console devolve pra home:**

```
coverageState : "Bloqueada devido a acesso proibido (403)"
pageFetchState: ACCESS_FORBIDDEN
robotsTxtState: ALLOWED
lastCrawlTime : 2026-08-17T07:02:50Z
crawledAs     : MOBILE
```

`robotsTxtState: ALLOWED` é a parte que importa: **não é o robots.txt**. O robots.txt do repositório está correto e libera o Googlebot. É o servidor devolvendo 403 pro IP verificado do Google, na hora do rastreio — hoje de manhã, inclusive.

**Estado das 16 URLs do sitemap:**

| Estado | Qtd | Quais |
|---|---|---|
| Indexada | 3 | nf-auto-correcao, nf-emissao-automatica, ml-cancelamentos |
| **403 no rastreio** | 5 | **home**, atendimento-insights, gym-app, motoboy-impressao, fretes-consolidado |
| "O Google não reconhece o URL" | 8 | cases, sobre, lucratividade, crm-por-dentro, crm-reativacao, hub-de-dados, romaneio-scanner, tray-frete |

As 3 que ainda constam como indexadas têm último rastreio em 13/07 e 23/07 — ou seja, são as que o Google conseguiu ler **antes** do bloqueio começar. Elas caem do índice na próxima tentativa.

**Quando começou.** Impressões por dia mostram o corte:

- 18/07 a 31/07 (14 dias): **17 impressões**
- 01/08 a 06/08 (6 dias): **5 impressões**
- 07/08 a 14/08 (8 dias): **2 impressões**

### Causa confirmada no painel (17/08/2026)

Security → Analytics → Events, evento das 04:02:50 BRT de 17/08:

| campo | valor |
|---|---|
| Ruleset | Cloudflare Bot Management rules for all plans |
| **Rule** | **Block AI training crawlers** (`76c5c5f15fdc46bcb5d8807cc338cd69`) |
| Action | Block |
| IP / ASN | `66.249.68.4` · **AS15169 Google LLC** |
| Host / Path | nak.api.br `/` |
| User agent | `…(compatible; Googlebot/2.1; +http://www.google.com/bot.html)` |

04:02:50 BRT = 07:02:50 UTC, que é exatamente o `lastCrawlTime` que a API do GSC devolveu pra home. **É o mesmo evento visto dos dois lados** — não sobra dúvida sobre a causa.

A tela AI Crawl Control → Security mostra por quê:

| crawler | categoria da Cloudflare | estado em 17/08 |
|---|---|---|
| **Googlebot** | Search Engine Crawler | 🔴 **bloqueado** |
| **BingBot** | Search Engine Crawler | 🔴 **bloqueado** |
| Applebot | AI Search | 🔴 bloqueado |
| Claude-User | AI Crawler | 🔴 bloqueado |
| Claude-SearchBot, OAI-SearchBot, PerplexityBot | AI Search | ✅ liberado |
| ChatGPT-User, Perplexity-User | AI Assistant | ✅ liberado |
| GPTBot, ClaudeBot, CCBot, Bytespider, Amazonbot, Meta-ExternalAgent | AI Crawler | ✅ bloqueado |
| Baidu | Search Engine Crawler | ✅ liberado |

Ou seja: `Training = Block`, salvo em 01/08 pra proteger o conteúdo de treinamento, levou junto **os dois buscadores** — e o Bing estava fora do índice pelo mesmo motivo que o Google, sem ninguém notar. O Baidu, da mesma categoria, passou ileso. Isso mostra que não foi decisão nossa nem regra coerente: foi a categorização da Cloudflare aplicada bot a bot.

**Por que não dava pra ver daqui:** a Cloudflare reconhece bot verificado por **IP**, não por User-Agent. `curl -A Googlebot https://nak.api.br/` responde **200** desta máquina, porque este IP não é o Google. O limite já estava anotado na verificação de 01/08 — e é justamente por isso que aquele teste passou: ele nunca poderia ter pego este bloqueio.

### Resolvido no mesmo dia (17/08/2026)

**O que NÃO funcionou, e por quê:** a primeira tentativa foi uma regra WAF custom com ação **Skip** em `cf.verified_bot_category in {"Search Engine Crawler" "AI Search"}`, pulando "All managed rules". A regra casou — e o bloqueio aconteceu assim mesmo. A prova é o **mesmo Ray ID** (`a2ca70fea932c96d`) aparecendo duas vezes nos eventos: uma como `Skip` (Custom rules), outra como `Block` (Managed rules). Os componentes puláveis oferecidos são Zone Lockdown, User Agent Blocking, Browser Integrity Check, Hotlink Protection, Security Level e as versões antigas de managed/rate limiting — **o ruleset de Bot Management não está na lista**. Não dá pra abrir exceção pra ele por WAF neste plano. Regra apagada.

**O que funcionou:** trocar o eixo de controle, de categoria pra lista por bot.

1. `Training` deixou de ser `Block` e virou `Allow (do not block)` — isso destrava os toggles por crawler, que ficam inertes enquanto a categoria manda.
2. Bloqueio individual, um a um: **GPTBot, ClaudeBot, Amazonbot, Bytespider, CCBot, Claude-User, Meta-ExternalAgent**.
3. `Search` e `Agent` seguem `Allow`.

**Verificado pelo lado do Google**, não por curl: Inspeção de URL → Testar URL ao vivo, às 14:34 e de novo às 14:48 depois de todas as mudanças → **"O URL está disponível para o Google · É possível indexar a página"**.

**Sitemap destravado junto:** reenviado e reprocessado no mesmo dia. Passou de `última leitura 31/05, 5 páginas` para **`última leitura 17/08, 16 páginas`**. Indexação da home solicitada manualmente.

**O que essa correção custou, registrado de propósito:** com o controle na lista e não na categoria, crawler de treino **novo** não nasce mais bloqueado. Ficaram liberados hoje, todos na categoria "AI Crawler" da Cloudflare: `Anchor Browser`, `Cloudflare Crawler`, `FacebookBot`, `Google-CloudVertexBot`, `Novellum AI Crawl`, `PetalBot`, `ProRataInc`, `TikTok Spider`, `Timpibot`. Nenhum deles está no `robots.txt`. Decidir se entram na lista de bloqueio — e revisar a lista a cada check mensal, porque agora ela é manutenção, não configuração.

**Divergência em aberto:** `Claude-User` está bloqueado no painel e `Allow` no `robots.txt` do repositório. A Cloudflare classifica como "AI Crawler"; o repo trata como assistente. Um dos dois tem que ceder.

## 🔴 Achado 2: o sitemap não é lido desde 31/05

A API devolve, pra `https://nak.api.br/sitemap.xml`:

```
lastDownloaded: 2026-05-31   |   web: 5 URLs enviadas   |   0 erros, 0 avisos
```

O arquivo tem **16 URLs** hoje. O Google conhece **5** — as de maio. Isso é independente do 403 (a última leitura é de muito antes) e explica sozinho as 8 URLs em "o Google não reconhece o URL": os cases publicados de junho pra cá nunca foram anunciados a ninguém.

Já sabíamos desde 14/06 que "o Google só busca o sitemap em ciclos próprios". O que não sabíamos é que o ciclo dele pode ser de **mais de dois meses**. Reenviar o sitemap no GSC a cada publicação deixa de ser opcional e vira parte do fluxo de publicar case.

## Ferramenta de medição

`.tools/gsc.py` (criado 17/08/2026) lê o Search Console pela API: desempenho 28d contra os 28d anteriores, top queries, top páginas, status do sitemap e inspeção de URL das 16 URLs do sitemap. Substitui a conferência manual página a página no painel, que era o único jeito de ver o estado real de indexação.

```
D:\Claude\cte_drive\.venv\Scripts\python.exe .tools\gsc.py
```

Token OAuth em `.tools/gsc_token.json` (fora do git). O cliente OAuth é reusado do `tiny_hub` e pertence a um projeto GCP de outra conta, onde a API não pode ser ligada — por isso o script manda o header `x-goog-user-project` pro projeto `angelic-artwork-357614`, da conta kashinha, onde a Search Console API foi habilitada em 17/08.

## Pendências técnicas (não-urgentes)

- [ ] **404.html não servido em prod** — confirmado de novo em 24/08: `/rota-inexistente` devolve **status 404 com corpo vazio (0 bytes)**. O status está certo, a página não existe pro visitante. Configurar `wrangler.toml` ou Worker custom (mexer com cuidado, risco de quebrar deploy).
- [ ] **Cache-Control max-age=0** — atualmente cada request revalida no Cloudflare. Configurar Cache Rules pra cachear assets/HTML por X tempo. Custo grátis então low priority.
- [ ] **Imagem Open Graph real** — atualmente OG/Twitter Cards apontam pra texto. Gerar imagem 1200x630 dinâmica por case (Apps Script com SVG, ou serviço tipo og-image).
- [x] **Cloudflare Web Analytics** — ~~pra medir tráfego total~~ **já instalado**: beacon `c48dfb70ce8140ffa8ad30637454ad88` presente nas 16 páginas, coletando. Pendência real virou **acesso de leitura**: sem API token da conta kashinha com `Account Analytics: Read`, o dado existe e não é consultável de fora do painel. Sem isso, todo check mensal fica cego pra tráfego direto, referral e visita de IA — que é justamente o sinal 2 da medição de GEO.

## Tabela de medições

| Data | Pgs indexadas | Impressões 28d | Cliques 28d | Posição média | Notas |
|------|---------------|----------------|-------------|---------------|-------|
| 2026-05-17 | 0 | 0 | 0 | — | Marco zero |
| 2026-05-24 | 3 (real) / 1 (report) | — | — | — | Check 1 semana. Sitemap processado (Google leu 24/05). Relatório agregado mostra 1 indexada por lag de 7d, mas inspeção individual revelou 3 indexadas (home, atendimento-insights, fretes-consolidado) e 2 pendentes (motoboy, ml-cancelamentos) — pedi indexação manual das 2 pendentes. 0 erros. Bing ainda em "Processing", sem 1ª varredura. |
| 2026-05-31 | 3 (mesmas do check anterior) | — | — | — | Check 2 semanas. **ACHADO CRÍTICO:** GSC reportou "Erro de redirecionamento" no motoboy. Investigação revelou que TODAS URLs `.html` retornavam 307 → versão sem `.html`. Sitemap apontava `.html`, confundindo Googlebot. Fix: removido `.html` de sitemap, canonical, og:url, schema, links internos. Gerador.gs atualizado. Sitemap re-enviado no GSC. Inspeção das 2 URLs sem `.html` (motoboy + ml-cancelamentos) confirmou que erro de redirect sumiu — agora "Detectada, mas não indexada" (estado normal). Indexação manual solicitada nas duas. Aguardar 7 dias pra medir efeito real. |
| 2026-06-07 | 5+ (inspeção) / 3 (report) | **8** | 0 | 23.1 | Check 3 semanas. **Experimento do fix .html confirmado** — motoboy + ml-cancelamentos agora "URL está no Google" via inspeção individual. Report agregado ainda mostra 3 indexadas + 5 não indexadas por causa do lag de 7d (motivos antigos: erro de redirect 2, canonical alternativo 2, redirect 1 — todos pré-fix). **Primeiras impressões reais: 8 em 7 dias** (saiu do zero). 0 cliques (esperado, posição média 23). Top query "nacl web plug in" — irrelevante, Google ainda explorando termos. **Bing finalmente saiu do Processing** — sitemap status "Success", 7 URLs descobertas, last crawl 06/06. |
| 2026-06-14 | 5 (report) / 5 confirmadas inspeção | **13** | 0 | **12.8** | Check 4 semanas (última semanal). **Posição média DESPENCOU de 23.1 → 12.8** (de 3ª pra 2ª página do Google). Impressões cresceram +62% (8→13). 5 do sitemap antigo indexadas. **2 cases novos (nf-auto-correcao, nf-emissao-automatica) publicados em 31/05 ainda NÃO indexados** — Google ainda diz "não reconhece o URL" depois de 2 semanas, sitemap ainda não foi re-rastreado pelo Google. Solicitação manual de indexação feita pras 2 hoje. **Bing voltou pra Processing** (sitemap mudou de 5 pra 7 URLs, está re-processando). Top queries: vazio. |
| 2026-06-17 | 7 indexadas (inspeção) | **27** | 0 | **16.1** (28d) | **Check Mês 1.** Janela mudou pra 28d. **🎯 Atendimento e ML cancelamentos entraram na 1ª PÁGINA do Google** (posições 7.0 e 8.9). NF Auto Correção e NF Emissão Automática indexaram em ≤3 dias após solicitação manual de 14/06 — confirma que request manual acelera. Gym App publicado em 15/06, solicitado hoje (esperar 7d). URLs antigas com .html ainda aparecem no índice (fretes-consolidado.html pos 9.7, atendimento-insights.html pos 2.0) — vão consolidar via canonical eventualmente. Top queries: "na api" (pos 7), "script expansão noturno" (pos 53), "nacl web plug in" (pos 70) — ainda exploratório, sem termos relevantes do nicho. **0 cliques** — esperado: queries são irrelevantes, ninguém que clicasse iria converter. |
| 2026-08-17 | **3 de 16** (API) | **24** | **1** | **15.0** | **Check Mês 3. Medido pela API (`.tools/gsc.py`), não pelo painel.** Mês 2 (17/07) não foi feito. **🔴 Googlebot tomando 403 desde ~04/08** — 5 URLs com `ACCESS_FORBIDDEN` e último rastreio de hoje, `robotsTxtState: ALLOWED` (não é o robots.txt). Impressões caíram 48→24; posição "melhorou" 31.7→15.0 porque as páginas mal posicionadas saíram do índice. **🔴 Sitemap sem releitura desde 31/05** — Google conhece 5 URLs, o arquivo tem 16; daí 8 URLs em "não reconhece o URL". **1º clique da história em 24/07** (`gym-app`, posição 5). Queries do período: 4, todas ruído, posições 47-51. Origem: 20 BR, 3 US, 1 FR. Diagnóstico de conteúdo do Mês 3 **adiado** — não se conclui nada sobre nicho com o rastreio bloqueado. **Os dois corrigidos no mesmo dia** (ver seções acima): rastreio liberado às 14:48 e sitemap relido com 16 páginas. |
| 2026-08-24 | **14 de 16** (API) | 19 | 0 | 15.4 | **Check de 1 semana pos-correcao do 403.** **A correcao funcionou no que ela podia resolver: rastreio.** Indexacao saltou de **3/16 para 14/16** — as 11 URLs que o Google 'nao reconhecia' foram rastreadas entre 18 e 21/08 e entraram no indice. Sobram 2: `hub-de-dados` ('Detectada, mas nao indexada') e `romaneio-scanner` ('Rastreada, mas nao indexada' em 18/08). Sitemap relido em **23/08**, 16 URLs, 0 erros — o ciclo de leitura voltou ao normal. **O que a correcao NAO resolveu, e nao ia resolver: demanda.** Impressoes pos-correcao (18 a 21/08) = **2 em 4 dias**, contra 1,2/dia no periodo pre-bloqueio. Zero clique desde 24/07. Em 60 dias o pico diario foi 6 impressoes. Nenhuma query relevante: a unica do periodo de 28d e 'script expansao noturna' na posicao 49. **Leitura: o 403 escondia o problema real, nao era o problema real.** Com o rastreio restaurado, o teto do site aparece — e o teto e baixo porque nao existe mencao externa nenhuma. Posicao media 15.4 sobre um conjunto que voltou a crescer (era 15.0 sobre 3 paginas), entao desta vez a media e comparavel pra baixo, nao pra cima. Melhor pagina: `atendimento-insights`, posicao 3,6 com 7 impressoes. Auditoria tecnica no mesmo dia (`auditoria-seo-geo`): **0 erros, 34 avisos**, todos de julgamento. Trafego total (Cloudflare Web Analytics) **nao medido** — o beacon esta em todas as 16 paginas e coletando desde sempre, mas falta token de leitura da conta. |
