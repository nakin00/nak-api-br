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

### Mês 3 (até 17/ago/2026)
**Objetivo:** primeira tração ou diagnóstico precoce.

- [ ] Impressões mensais: __ (anotar)
- [ ] Cliques mensais: __
- [ ] Páginas indexadas: __ (deveriam ser 100% das submetidas)
- [ ] Posição média das 10 queries mais frequentes: __
- [ ] Existe alguma query com posição < 20? (significa que está concorrendo, mesmo que ainda não converte)

**Se em 3 meses tudo ainda for zero:** revisar conteúdo. Provavelmente os termos escolhidos não têm volume de busca, ou o site não tem autoridade suficiente pra concorrer com o que já existe.

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
| 2026-05-31 | Remover `.html` de todas URLs (sitemap, canonical, og:url, schema, links internos). Cloudflare Workers fazia redirect 307 automático que confundia o Googlebot. | Sem o redirect, motoboy e ml-cancelamentos indexam em ≤7 dias. As 2 já indexadas (atendimento, fretes) mantêm indexação após cache do Google atualizar (pode haver flutuação temporária). | __ |

## Insights de processo (observações que viram conteúdo no case)

- **2026-05-24:** O relatório agregado "Indexação > Páginas" do GSC tem ~7 dias de lag. Mostrou 1 indexada quando inspeção individual revelou 3. Sempre cross-checar com Inspeção de URL pra estado real.
- **2026-05-24 (hipótese a confirmar):** Google parece priorizar indexação de páginas com conteúdo mais rico/estruturado. As 2 primeiras a indexar foram as com 4 visuais (atendimento-insights) e dashboard no hero (fretes-consolidado). As 2 pendentes têm hero mais simples (só logs). Testar se essa correlação se mantém em cases futuros.
- **2026-05-31:** A hipótese de "conteúdo denso" acima estava **errada**. Investigação na 2ª semana mostrou que TODAS as URLs `.html` retornavam **307 redirect** pra versão sem `.html` (feature do Cloudflare Workers/Pages). Sitemap apontava pra `.html`, então Googlebot batia em redirect toda vez. As 2 que indexaram (atendimento e fretes) foram pura sorte do crawler ter seguido o redirect daquela vez. Insight: **erro técnico se disfarça de padrão**. Sempre verificar o raw HTTP behavior antes de inferir comportamento de algoritmo. Esse é exatamente o tipo de "data não-rigoroso" que viraria conclusão falsa num case escrito sem investigação técnica.
- **2026-05-31:** Quando o GSC fala "Erro de redirecionamento", ele está dizendo algo CONCRETO. Não é apenas "demora pra indexar". É problema técnico que deve ser investigado com `curl -v` ou equivalente antes de fazer mudança de conteúdo.
- **2026-05-31 (pente fino completo):** Após achar o bug do `.html`, fizemos varredura completa pra checar se havia mais. Encontramos: (1) os 24 links internos pra home (`../index.html`) ainda usavam `.html` — corrigi pra `../`. (2) HTTP não força HTTPS (Cloudflare config a fazer). (3) `www.nak.api.br` não resolve. (4) Titles e meta descriptions excediam limites de SERP (60 e 160 chars) — todos reescritos abaixo do limite mantendo termos buscáveis. (5) 404 padrão do Cloudflare era genérica — criada `/404.html` com estética do site. Lição: ao achar um bug técnico, o pente fino imediato vale mais que esperar próximo check.

## Tabela de medições

| Data | Pgs indexadas | Impressões 28d | Cliques 28d | Posição média | Notas |
|------|---------------|----------------|-------------|---------------|-------|
| 2026-05-17 | 0 | 0 | 0 | — | Marco zero |
| 2026-05-24 | 3 (real) / 1 (report) | — | — | — | Check 1 semana. Sitemap processado (Google leu 24/05). Relatório agregado mostra 1 indexada por lag de 7d, mas inspeção individual revelou 3 indexadas (home, atendimento-insights, fretes-consolidado) e 2 pendentes (motoboy, ml-cancelamentos) — pedi indexação manual das 2 pendentes. 0 erros. Bing ainda em "Processing", sem 1ª varredura. |
| 2026-05-31 | 3 (mesmas do check anterior) | — | — | — | Check 2 semanas. **ACHADO CRÍTICO:** GSC reportou "Erro de redirecionamento" no motoboy. Investigação revelou que TODAS URLs `.html` retornavam 307 → versão sem `.html`. Sitemap apontava `.html`, confundindo Googlebot. Fix: removido `.html` de sitemap, canonical, og:url, schema, links internos. Gerador.gs atualizado. Sitemap re-enviado no GSC. Inspeção das 2 URLs sem `.html` (motoboy + ml-cancelamentos) confirmou que erro de redirect sumiu — agora "Detectada, mas não indexada" (estado normal). Indexação manual solicitada nas duas. Aguardar 7 dias pra medir efeito real. |
