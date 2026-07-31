# Melhorias — nak.api.br

Lista viva de melhorias mapeadas, priorizadas por impacto vs esforço. Atualizada em 21/06/2026.

Regra: item só sai daqui quando FEITO e VALIDADO, ou quando decidirmos conscientemente não fazer (aí documenta o porquê).

---

## 🔴 P0 — Bloqueio ativo (só resolve no painel Cloudflare)

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

---

## ❌ Decididas contra (com motivo)

| Data | Ideia | Por quê não |
|---|---|---|
| 15/06 | Redirect rule `/insta` → UTM | Cloudflare Redirect Rules strippava query string do target. Complicação > benefício. Insta esconde URL feia atrás de botão, então UTM cru resolve. |
| 31/05 | Anonimizar transportadoras (Jadlog etc) | São empresas públicas do mercado, não expõem a operação. Nomes ajudam SEO. |
