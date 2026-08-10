# Melhorias — nak.api.br

Lista viva de melhorias mapeadas, priorizadas por impacto vs esforço. Atualizada em 21/06/2026.

Regra: item só sai daqui quando FEITO e VALIDADO, ou quando decidirmos conscientemente não fazer (aí documenta o porquê).

---

## 🔴 P0 — Bloqueio ativo (só resolve no painel Cloudflare)

### 0. ~~O site é invisível pra IA de busca~~ ✅ RESOLVIDO 01/08
Destravado no painel: `Training = Block` / `Search` e `Agent` = Allow, regra legada "Block AI bots" desligada e "Managed robots.txt" desligado. Bots de busca passaram a 200, treino segue bloqueado, internos seguem atrás de login. Detalhe do que mudou e o estado verificado estão no `SEO_BASELINE.md`. **Volta na agenda em 15/09/2026**, quando a Cloudflare passa a bloquear crawlers de propósito misto (GPTBot, ClaudeBot) junto com os de treino.

<details><summary>Diagnóstico original (mantido pro histórico)</summary>

### 0. O site é invisível pra IA de busca — duas camadas bloqueando
**Descoberto em 31/07/2026.** Objetivo declarado: ser lida e citada por assistente de IA, sem liberar treinamento.

Duas travas independentes, as duas herdadas de padrão do Cloudflare (ninguém ligou de propósito):

1. **WAF / AI bot block** — `GPTBot`, `ClaudeBot`, `PerplexityBot`, `OAI-SearchBot` e `meta-externalagent` recebem **403** no edge. User-agent qualquer recebe 200. Nenhum modelo consegue ler o site.
2. **robots.txt gerenciado** — o Cloudflare injeta um bloco *antes* do nosso, com `Disallow: /` pra GPTBot, ClaudeBot, Google-Extended, CCBot, Bytespider, Amazonbot, Applebot-Extended e `Content-Signal: ai-train=no`. Como vem primeiro, nosso arquivo não consegue sobrescrever — no Google-Extended os dois se contradizem hoje.

**Ação (painel, zona `nak.api.br`):**
- [ ] Security → Bots → *AI Scrapers and Crawlers* → desligar
- [ ] Security → WAF → Custom rules → **Skip** com `hostname eq "nak.api.br"` (mantém `frete`, `central`, `status`, `print-pulse`, `gym` bloqueados)
- [ ] AI Crawl Control → *Managed robots.txt* → desligar (aí o `/robots.txt` do repo passa a valer)

**Esforço:** baixo (3 toggles) · **Impacto:** alto — é pré-requisito de tudo em GEO
**Validar depois:** `curl -A "OAI-SearchBot/1.0" https://nak.api.br/` tem que dar 200, e `curl -A "GPTBot/1.2"` pode continuar bloqueado (é o de treino).

</details>

### 0b. ~~Tabela de frete exposta em `frete.nak.api.br`~~ ✅ FEITO 31/07
Achado no mesmo pente fino: `?test=1` rodava antes da validação de token e devolvia as regras de frete inteiras (CEP, peso, preço, prazo) pra qualquer um com a URL. Corrigido e no ar — modo teste exige `TRAY_TOKEN`, nega se o secret não existir, raiz não conta mais as regras, `/robots.txt` com `Disallow: /`. Caminho da cotação intacto. Ver repo `tray_frete`.

---

## 🔴 P1 — Alto impacto, faz logo

### 1. Backlinks externos (o gargalo real do SEO agora)
**Problema:** site rankeia na 1ª página mas pra queries irrelevantes ("na api", "nacl web plug in"). Google não tem sinais externos pra saber do que o site trata. 0 backlinks conhecidos.
**Ação:**
- [ ] 1 post no LinkedIn linkando pra um case específico (não a home) — texto curto contando a dor real
- [ ] Repetir a cada case novo publicado (vira rotina da cadência quinzenal)
- [ ] Bio do LinkedIn e Instagram com link (feito, manter)
**Esforço:** baixo (30min por post) · **Impacto:** alto — é o que falta pro Google entender o nicho
**Meta mensurável:** no check Mês 2 (17/jul), ver se as queries começam a incluir termos do nicho (tiny, apps script, whatsapp, nf)

### 2. Publicar ML Etiquetas (case do dia 21/06 — em andamento)
**Status:** perguntas enviadas pra Jaque, aguardando respostas (por que marcar impressa, volume, tempo economizado, quando começou)
**Esforço:** médio · **Impacto:** mantém cadência quinzenal

---

## 🔴 P1 — Achados do pente fino de 01/08

### A. ~~URLs `.html` antigas redirecionam com 307, não 301~~ ✅ FEITO 01/08
**Era:** `/cases/x.html`, `/index.html`, `/sobre.html` respondiam **307** (temporário). O registro de 31/05 dizia corrigido — não estava, só a URL nova passou a funcionar. 307 faz o Google manter a URL velha no índice e **não transferir autoridade**. Batia com Googlebot acumulando 601 requisições malsucedidas em 24h num site de 15 páginas.

**Resolvido com duas Redirect Rules** (o 307 vem do handler de assets do Worker e não é configurável; regra explícita ganha dele, porque roda antes):

| Regra | Filtro | Destino |
|---|---|---|
| `.html para URL sem extensao (301)` | `ends_with(uri.path, ".html") and not ends_with(uri.path, "/index.html")` | `wildcard_replace(full_uri, "https://nak.api.br/*.html", "https://nak.api.br/${1}")` |
| `index.html para raiz (301)` | `uri.path eq "/index.html"` | `https://nak.api.br/` (estático) |

Ambas 301, com *preserve query string* ligado (não perde UTM de link antigo).

**Por que duas e não uma:** a primeira tentativa usou `regex_replace`, que dava pra resolver os dois casos numa regra só. A Cloudflare recusou — **`regex_replace` exige plano Business**, e a zona é free. `wildcard_replace` é liberado no free, mas transformaria `/index.html` em `/index` (404). Daí o `index.html` sair por exclusão na primeira regra e ganhar a sua própria.

### D. ~~IndexNow~~ ✅ FEITO 01/08
Crawler Hints ligado em Caching → Configuration. Avisa Bing e Yandex na hora que uma página muda, em vez de esperar o crawler passar. Ligar implica concordar com os Supplemental Terms da Cloudflare pro recurso e compartilhar a informação de quais URLs mudaram.

### B. Dois cases curtos demais
`fretes-consolidado` (693 palavras) e `ml-cancelamentos` (685). Os outros têm de 1.000 a 3.100. Abaixo de ~800 o texto não sustenta long-tail.
**Ação:** ampliar com o que falta nos dois — decisão técnica, o que deu errado, número atualizado.
**Esforço:** médio (precisa de dado real) · **Impacto:** médio

### C. Barra final redireciona com 307
`/cases/tray-frete/` → 307. Sobrou: a regra do item A casa por `.html`, e a barra final não tem extensão. Impacto baixo (nada linka com barra), mas fica anotado.

### E. Bing / Yahoo — pendente com ela
Yahoo não tem índice próprio desde 2009: quem serve é o Bing. Então "aparecer no Yahoo" = aparecer no Bing, que também alimenta o Copilot. **Bing Webmaster Tools** aceita importar do Search Console e dá dado de indexação que não existe de outra forma. Segue como item do `SEO_PLAYBOOK` desde maio.

---

## 🟠 P2 — Impacto médio, quando der

### 3. ~~Imagem Open Graph real (1200×630 por case)~~ ✅ FEITO 18/07
9 imagens geradas via PowerShell System.Drawing (template dark com categoria + título + logo), servidas em `/og/{slug}.png`. Meta og:image + twitter:image em todas as páginas. Gym em roxo, hub em verde, resto azul. Script em scratchpad (regenerar quando publicar case novo — lembrar de adicionar a linha no script).

### 4. Cache-Control decente
**Problema:** `max-age=0, must-revalidate` — toda request revalida na edge. Latência já é boa (~90ms) mas seria melhor com cache.
**Ação:** Cache Rule no Cloudflare: HTML com `max-age=300` (5min) é suficiente — deploy leva ~30s então janela de conteúdo velho é curta.
**Esforço:** baixo (1 rule no painel) · **Impacto:** baixo-médio (site já é rápido)

### 5. 404 personalizada não é servida
**Problema:** `404.html` existe no repo desde 31/05 mas Cloudflare Workers (assets) não usa automaticamente. Visitante de URL errada vê página genérica do Cloudflare.
**Ação:** configurar `not_found_handling` no wrangler config do Worker — CUIDADO: mexer em config de deploy tem risco, testar em preview antes.
**Esforço:** médio (risco de quebrar deploy) · **Impacto:** baixo (pouca gente cai em 404)

---

## 🟡 P3 — Backlog, sem pressa

### 6. Página de categoria/filtro de cases
Quando tiver 10+ cases, a home vai ficar longa. Filtro por categoria (Operação, Fiscal, Atendimento, Pessoal) ou páginas por categoria.
**Gatilho:** revisitar quando publicar o 10º case.

### 7. RSS feed
Pra quem quiser acompanhar por leitor de feed. Nicho técnico gosta.
**Esforço:** baixo (gerar XML estático no mesmo fluxo do sitemap).

### 8. Dark/light mode toggle
Site é dark-only. Alguns leitores preferem light pra ler texto longo.
**Contra:** quebra identidade visual. Decidir com calma.

### 9. Automação de changelog
Hoje o changelog "em movimento" é atualizado manual no HTML. Podia sair do git log filtrado.
**Gatilho:** quando o gerador.gs (Apps Script) entrar em uso de verdade.

### 10. Busca no site
Só faz sentido com 15+ cases. Pagefind ou similar (estático, sem backend).

---

## 🔵 Subdomínios internos fora do índice (feito 10/08)

**Problema:** a propriedade do GSC é do tipo **Domínio**, então monitora `nak.api.br` E todos os subdomínios. Os apps internos (login-protected) não tinham `robots.txt` — todos serviam o HTML da aplicação no lugar. Google tentava rastrear, batia na barreira de login, reportava **403** e poluía o relatório de indexação com 4 páginas de erro que não têm nada a ver com o site público.

**Resolvido:**

| Subdomínio | Arquitetura | Como | Status |
|---|---|---|---|
| status | Worker | rota `/robots.txt` no fetch | ✓ |
| vendedor | Worker | rota `/robots.txt` no fetch | ✓ |
| print-pulse | Worker | rota `/robots.txt` no fetch | ✓ (subiu no deploy de outra sessão) |
| gym | CF Pages | arquivo `robots.txt` na raiz | ✓ |
| romaneio | CF Pages | arquivo `public/robots.txt` | ✓ |
| central | CF Pages + **Access** | ✗ — Access intercepta ANTES do Pages, `/robots.txt` nunca chega | pendente |

**Sobre o central:** o Cloudflare Access barra tudo antes do conteúdo, então não dá pra servir `robots.txt` por lá. Duas saídas: (a) criar policy de **Bypass** no Access só pro path `/robots.txt`, ou (b) aceitar — o Access barrando é o comportamento correto de segurança, e o ruído no relatório some com a propriedade "Prefixo de URL" no GSC. Ficamos em (b) por ora; (a) só se o relatório continuar incomodando.

**Regra pra apps futuros em subdomínio:** todo app interno nasce com `robots.txt` = `Disallow: /`. Worker → rota no início do fetch, antes de qualquer auth. Pages → arquivo estático.

## 📊 Instrumentação (acompanhar, não agir)

### 11. Cloudflare Web Analytics
Instalado em 15/06 (snippet em todas as páginas). Ainda acumulando dados.
- [ ] Olhar primeiro relatório de origens no check Mês 2 (17/jul) — ver se UTMs de Insta/LinkedIn aparecem

### 12. GSC — cadência mensal
Próximo check: 17/jul (Mês 2). Cadência mensal daqui pra frente.
- Pergunta-chave do Mês 2: as queries mudaram de aleatórias pra termos do nicho? (depende do P1)

---

## ✅ Feitas (histórico)

| Data | Melhoria |
|---|---|
| 31/05 | Fix crítico: URLs sem `.html` (redirect 307 quebrava indexação) |
| 31/05 | Titles ≤60 chars, descriptions ≤160 chars em todas páginas |
| 31/05 | Always Use HTTPS + CNAME www + redirect www→apex |
| 31/05 | Links internos `../index.html` → `../` (24 ocorrências) |
| 15/06 | Cloudflare Web Analytics em todas as páginas |
| 15/06 | Badges "em produção desde X" nos 7 cases |
| 15/06 | Changelog "em movimento" na home |
| 21/06 | Esta lista |
| 18/07 | Imagem Open Graph real (1200×630) por case |
| 31/07 | `llms.txt` — índice legível por máquina, 11 cases agrupados por área |
| 31/07 | `/sobre` — página de entidade (autor, regra do case, stack, licença de citação) |
| 31/07 | `robots.txt` novo: libera bots que citam, bloqueia os de treino, `Content-Signal` |
| 31/07 | Schema: `dateModified` real, autor como `Person` com URL, `publisher`, `isPartOf`, `image`, `BreadcrumbList` nos 11 cases |
| 31/07 | Home: `WebSite` enriquecido + `CollectionPage` listando os 11 cases |
| 01/08 | Painel Cloudflare destravado (ver `SEO_BASELINE.md`) |
| 01/08 | `sameAs` ligando GitHub, LinkedIn e Instagram, em schema e link visível |
| 01/08 | Novo case `tray-frete` |
| 01/08 | Titles ≤60 e descriptions ≤160 em todas as páginas (tinham regredido em 14 páginas) |
| 01/08 | `/cases` — índice por área, que antes dava 404 |
| 01/08 | `sitemap.xml` com `lastmod` real, gerado por `gerar_sitemap.mjs` a partir do git |

---

## ❌ Decididas contra (com motivo)

| Data | Ideia | Por quê não |
|---|---|---|
| 15/06 | Redirect rule `/insta` → UTM | Cloudflare Redirect Rules strippava query string do target. Complicação > benefício. Insta esconde URL feia atrás de botão, então UTM cru resolve. |
| 31/05 | Anonimizar transportadoras (Jadlog etc) | São empresas públicas do mercado, não expõem a operação. Nomes ajudam SEO. |
