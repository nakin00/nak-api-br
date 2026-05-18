# SEO Playbook — nak.api.br

Princípios de SEO aplicados no site. Documento vivo. Vira case publicado depois ("Como saí de 0 a X visitas orgânicas em N meses").

## Princípio mestre

SEO não pode quebrar o `ANTI_IA.md`. Se uma técnica de SEO exige escrever "as melhores automações para empresas modernas", a técnica está errada — não a regra.

Conteúdo bom rankeia. Conteúdo otimizado pra robô e ruim pra humano não rankeia mais (e quando rankeia, não converte).

## O que já está feito (técnico)

- [x] `robots.txt` permitindo tudo + apontando sitemap
- [x] `sitemap.xml` listando home + cases (atualizar quando publicar novo case)
- [x] Meta `description` em cada página, ~150-160 chars, com gatilho de clique
- [x] Meta `keywords` com termos reais que pessoas digitam
- [x] `<link rel="canonical">` em todas páginas (evita duplicate content)
- [x] Open Graph (compartilhamento Facebook/WhatsApp/LinkedIn)
- [x] Twitter Cards
- [x] Schema.org JSON-LD `TechArticle` em cases, `WebSite` na home
- [x] `<html lang="pt-BR">` em todas páginas
- [x] Mobile-first responsive
- [x] CSS inline (zero render-blocking)
- [x] Cloudflare CDN (latência global baixa)
- [x] HTTPS (Cloudflare auto)
- [x] URLs descritivas (slugs em vez de IDs)
- [x] Heading hierarchy correta (h1 único por página, h2/h3 estruturados)
- [x] Internal linking — bloco "Cases relacionados" no fim de cada case

## O que falta fazer

### Você
- [ ] Criar conta **Google Search Console** (https://search.google.com/search-console)
- [ ] Verificar propriedade `nak.api.br` (via DNS TXT no Cloudflare — fácil)
- [ ] Submeter `https://nak.api.br/sitemap.xml`
- [ ] Repetir no **Bing Webmaster Tools** (https://www.bing.com/webmasters) — 30% do tráfego orgânico no Brasil em alguns nichos
- [ ] Adicionar Google Analytics 4 OU Cloudflare Analytics (medir resultado)

### Eu (em sessões futuras)
- [ ] Gerar imagem OG real (1200x630 com título do case + logo) — ferramenta tipo Cloudinary, ou Apps Script que gera SVG
- [ ] Schema `BreadcrumbList` em cases (Cases > Atendimento > ...)
- [ ] Schema `FAQ` em cases que tiverem perguntas comuns
- [ ] RSS feed dos cases (`/feed.xml`)
- [ ] Página `/sobre` ou `/manifesto` com história + autoridade
- [ ] Categorias como páginas (`/atendimento`, `/operacao`, `/financeiro`) com lista filtrada

## Princípios de conteúdo

### Titles (60-65 chars)
**Bom:** "Imprimir separação Motoboy do Tiny ERP automaticamente"
**Ruim:** "Solução completa de automação de impressão para e-commerce"

Title deve ter o termo que a pessoa digitaria. "Como fazer X com Y" funciona bem.

### Descriptions (150-160 chars)
**Bom:** "Python no PC da impressora ouvindo Tiny ERP a cada 30s. Pedido cai, papel sai, status atualiza, Slack avisa. Zero clique humano."
**Ruim:** "Aprenda a automatizar processos de impressão de forma eficiente e revolucionária com nossa solução completa."

Descrição é gatilho de clique no Google. Tem que ter PROMESSA CONCRETA + DESBLOQUEIO.

### Keywords
Use o que pessoa REALMENTE digita. Tools:
- Google Autocomplete (digita parte da query, vê sugestão)
- "Pessoas também perguntam" no Google
- AnswerThePublic.com
- Search Console (depois de ter dados)

Não invente keyword vazia. "automação inteligente" não busca. "tiny erp puxar pedido python" busca.

### Headings
H1 único por página (já é o `<h1>` do case-hero).
H2 nas seções principais (já são os "Dor operacional", "Impacto", etc).
H3 dentro das seções se precisar.

### Conteúdo
- Mínimo 1500 palavras por case (cases atuais têm ~1800-2200)
- Frases curtas (Flesch reading ease > 60)
- Listas (ranqueiam bem em "featured snippet")
- Negrito em palavras-chave dentro do texto (sem stuffing)
- Linkar pra outros cases relacionados

### Cadência
Google premia consistência. **1 case novo a cada 2-4 semanas** é melhor que 5 num mês e zero depois.

## Termos-alvo iniciais (por case)

### atendimento-insights
Termos primários: "apps script gemini atendimento", "análise emails ia", "automação atendimento ecommerce"
Termo cauda longa (long-tail): "como ler emails de atendentes automaticamente com IA"

### motoboy-impressao
Termos primários: "tiny erp impressora térmica python", "polling tiny api"
Long-tail: "como imprimir separação motoboy do tiny automaticamente"

### fretes-consolidado
Termos primários: "tiny erp frenet integração", "custo real frete por nf"
Long-tail: "como calcular margem real por pedido com frete embutido"

### ml-cancelamentos
Termos primários: "mercado livre api cancelamento", "alerta slack mercadolivre"
Long-tail: "alerta quando pedido pago é cancelado no mercado livre"

## Métricas de sucesso

Mês 1: indexação completa no Google (5 URLs em "Páginas indexadas" do Search Console)
Mês 2: primeiras impressões orgânicas
Mês 3: primeiras visitas orgânicas
Mês 6: 50+ visitas orgânicas/dia (depende de quantos cases foram publicados)

Vira case **quando tiver 6 meses de dados E resultado mensurável** (vide princípio 1 do ANTI_IA.md).

Se em 6 meses não tiver tração orgânica real, o aprendizado é outro: "como NÃO funcionou SEO num portal técnico de nicho" — também serve como case, mas honesto. Tentativa fracassada documentada com honestidade vale mais que tentativa em andamento vendida como sucesso.

## Anti-padrões (NÃO fazer)

- ❌ Keyword stuffing ("automação tiny erp automação tiny api automação...")
- ❌ Texto invisível ou camuflado pra SEO
- ❌ Backlinks comprados / PBN
- ❌ Pedir backlink em troca de backlink (Google detecta)
- ❌ Reescrever case existente só pra rankear melhor — melhor publicar case novo
- ❌ Title clickbait que não bate com conteúdo (alta taxa de bounce = penalização)
