# Posts de LinkedIn — nak.api.br

Objetivo: sair de zero menção externa ao domínio. Não é marketing de conteúdo, é deixar
texto indexável fora do próprio site dizendo do que o site trata.

Cada post responde **um dos 6 prompts fixos** do `SEO_BASELINE.md`. Mesma pergunta que a
gente mede uma vez por mês no ChatGPT/Perplexity. Se o post não responde a pergunta,
ele não serve pro que foi feito.

## Regras de formato

- Primeira linha é a pergunta literal. Sem gancho, sem "você sabia".
- O post responde sozinho. Nada de teaser com "link nos comentários".
- Números reais, sem nome de empresa. "Uma operação de e-commerce", nunca a marca.
- A URL vai **no corpo do post**, em texto puro, apontando pro case específico.
- Vale o checklist do `ANTI_IA.md` inteiro. É onde a voz de robô mais escapa.
- Sem carrossel, sem print com texto dentro. Imagem é ilegível pra quem indexa.

## Cadência

| # | Data | Prompt respondido | Case linkado |
|---|------|-------------------|--------------|
| 1 | ter 18/08/2026 | NF rejeitada pela SEFAZ por erro de cadastro | `/cases/nf-auto-correcao` |
| 2 | ter 01/09/2026 | Emitir NF automática para pedidos ML e Shopee | `/cases/nf-emissao-automatica` |
| 3 | ter 15/09/2026 | Reduzir custo de armazenamento do histórico do ERP | `/cases/hub-de-dados` |
| 4 | ter 29/09/2026 | Custo real de frete por nota fiscal | `/cases/fretes-consolidado` |
| 5 | ter 13/10/2026 | Imprimir separação do Tiny automaticamente | `/cases/motoboy-impressao` |
| 6 | ter 27/10/2026 | Alternativa barata a coletor de código de barras | `/cases/romaneio-scanner` |

Depois de cada post: anotar a data em `SEO_BASELINE.md` → "Experimentos registrados".
Sem a data anotada não dá pra atribuir efeito nenhum depois.

---

## Perfil (fazer uma vez, antes do primeiro post)

**Headline**

```
Automação de operação de e-commerce — Tiny ERP, NF-e, logística e dados | nak.api.br
```

**Seção "Sobre"** — mesma definição do `/sobre` e do `llms.txt`, de propósito. É a
repetição idêntica que faz a máquina entender que perfil e site são a mesma entidade.

```
Trabalho na operação de um e-commerce brasileiro de médio porte e automatizo o que
não deveria estar sendo feito na mão: emissão de nota fiscal, conferência de
expedição, custo real de frete, arquivo de histórico do ERP.

Publico cada automação em nak.api.br — a dor concreta, a decisão técnica, o que deu
errado no caminho e o número que sobrou no fim. Um texto só vira case quando está em
produção e tem resultado medido. Tentativa em andamento fica de fora.

Stack de custo baixo, quase tudo em plataforma gratuita: Google Apps Script,
Cloudflare Workers, D1, Python, Tiny ERP, Slack.
```

**Campo Website:** `https://nak.api.br`

O link do perfil e o link do post são `nofollow` — não passam autoridade pro Google. O
que conta é o domínio aparecer **escrito em texto**, no meio de um conteúdo que fala do
assunto. Por isso o `nak.api.br` está escrito no corpo do "Sobre" e no fim de cada post.

---

## Post 1 — NF rejeitada pela SEFAZ

*Publicar 18/08/2026 · aponta pra `/cases/nf-auto-correcao`*

```
O que fazer quando a nota fiscal é rejeitada pela SEFAZ por erro de cadastro.

Na operação que eu toco são cerca de 2000 NFs por mês. 30% voltavam rejeitadas.

Quase sempre o mesmo motivo: pedido de pessoa jurídica com inscrição estadual
faltando, IE errada, ou bairro vazio no cadastro do cliente.

A correção manual era abrir a nota rejeitada no Tiny, apagar o CNPJ, colar de novo pra
ele rebuscar os dados, salvar, emitir. De 1 a 2 minutos por nota. Umas 15 horas por
mês de uma pessoa, sempre a mesma sequência de cliques.

O que resolveu não foi corrigir mais rápido. Foi parar de tratar caso a caso e montar
uma cascata de tentativas, nessa ordem:

1. Consulta o CNPJ numa base pública e pega a IE real
2. Se falhar, tenta uma segunda base como fallback
3. Se não existe IE ativa, marca como isento
4. Se nada bate, deixa vazio como não-contribuinte

Bairro vazio o ViaCEP resolve antes de chegar aí.

Uma pessoa só é chamada quando as quatro estratégias falham. E o aviso já diz qual
falhou e por quê.

Dois aprendizados que só vieram rodando:

A base de CNPJ tem limite de 3 consultas por minuto. Quando estourava, o bot entendia
"esse cliente não tem IE" e marcava isento. A SEFAZ recusava, porque o cliente era
contribuinte. Um falso isento virando rejeição nova. Cache de 24 horas por CNPJ
resolveu.

E tem estado que recusa a IE mesmo quando a base pública devolve ela como válida.
Bahia é o caso. Esse é manual de verdade — insistir só gera retrabalho.

Hoje 99% se corrige sozinho, o resto sai com um clique. Custo do bot: zero, roda em
Apps Script.

Escrevi o passo a passo completo, com os 14 endpoints que testei e não funcionaram,
em nak.api.br/cases/nf-auto-correcao
```

---

## Post 2 — Emissão automática de NF

*Publicar 01/09/2026 · aponta pra `/cases/nf-emissao-automatica`*

```
Como emitir nota fiscal automática para pedidos do Mercado Livre e da Shopee.

A atividade principal de uma pessoa aqui era emitir NF. Umas 4 horas por dia: abrir o
pedido aprovado, conferir, faturar, emitir, repetir. Cerca de 2000 vezes por mês.

O problema nem era o tempo. Era que o faturamento inteiro dependia de uma pessoa
estar lá. Se ela faltava, pedido não saía, porque pedido sem nota não pode sair.

Hoje isso é um trigger de tempo no Apps Script. Ele varre as contas do ERP atrás de
pedido aprovado e, pra cada um, faz o ciclo inteiro: valida o cadastro, corrige o que
estiver faltando, emite a nota, imprime a etiqueta quando o canal exige, registra numa
planilha e avisa no Slack se algo deu errado.

A primeira versão era "gera e torce". Emitia direto. 40% rejeitava na SEFAZ por
cadastro errado, e a pessoa que não emitia mais passou a corrigir rejeição. Troquei um
trabalho manual por outro.

A virada foi inverter a ordem: validar o cadastro ANTES de gerar a nota. PJ sem
inscrição estadual, consulta a base de CNPJ. Bairro vazio, ViaCEP. Corrige o contato,
depois emite.

Três coisas que me custaram tempo e talvez poupem o seu:

O endpoint que gera a nota a partir do pedido usa um retrato congelado do pedido, não
o cadastro atualizado do cliente. Corrigir o contato não bastava — a nota nascia com
os dados velhos do mesmo jeito. A saída foi arrumar na configuração de natureza de
operação, pra toda nota futura já nascer certa.

O token do Mercado Livre expira em 6 horas. O bot parava de imprimir etiqueta sem
avisar ninguém. Renovação automática pelo refresh token resolveu.

E validação preventiva não chega em 100%. Sempre sobra caso que rejeita. Por isso
existe um segundo bot, irmão desse, que cuida das rejeitadas. Um sozinho não fecha o
ciclo.

Resultado: 4 horas por dia devolvidas, faturamento rodando 24/7, custo mensal zero.

O caminho todo, incluindo as versões que não funcionaram, está em
nak.api.br/cases/nf-emissao-automatica
```

---

## Post 3 — Custo de armazenamento do ERP

*Publicar 15/09/2026 · aponta pra `/cases/hub-de-dados`*

```
Como reduzir o custo de armazenamento de histórico do ERP.

Eu estava pagando R$ 2.067 por mês só em extensão de banco de dados do ERP. Nota de
2022 que ninguém abre, pedido antigo de consulta eventual. R$ 24.806 por ano pra
guardar passado.

O ERP cobra o banco por bloco: o plano vem com 300 MB, e cada 500 MB extra custa
R$ 266,26 por mês. Cada ano de operação empilha mais uma extensão. É um custo que só
sobe.

Apagar não era opção. Nota fiscal tem obrigação legal de guarda, e histórico de
cliente tem valor comercial.

Montei um banco próprio fora do ERP: um Cloudflare Worker com D1 pro dado estruturado
e R2 pros XMLs das notas. O webhook do ERP joga o que é novo lá em tempo real, e um
importador em Python processa os ZIPs de backup pra levar o histórico antigo.

A comparação que decidiu tudo, pra guardar os mesmos 500 MB:

Extensão de banco no ERP — R$ 266,26/mês
Cloudflare D1, com 5 GB — cerca de R$ 30/mês

O ERP cobra umas 90 vezes mais caro pelo mesmo espaço. E isso não é crítica ao ERP:
banco de ERP é feito pra operação do dia, não pra arquivo morto. O erro era meu, usar
espaço operacional caro pra guardar histórico frio.

Com o histórico em três lugares (nuvem, ZIP local e Drive), aí sim veio o expurgo no
ERP, mês a mês. Cada exclusão passa por uma verificação automática antes: o dado está
no hub, o XML está arquivado, o backup existe. Só então libera.

Em 30 dias de expurgo as extensões caíram de R$ 2.067 para R$ 663 por mês. R$ 16.847
por ano, medido no boleto, não projetado.

Efeito colateral que eu não esperava: a busca ficou melhor que a do ERP. Como o hub
recebe todas as contas do grupo, dá pra procurar um CNPJ e ver o histórico inteiro
numa consulta só. No ERP cada conta é uma ilha.

A conta detalhada e o processo de expurgo seguro estão em nak.api.br/cases/hub-de-dados
```

---

## Post 4 — Custo real de frete por NF

*Publicar 29/09/2026 · aponta pra `/cases/fretes-consolidado`*

```
Como saber o custo real de frete por nota fiscal.

Se o seu produto sai com frete embutido no preço, você provavelmente não sabe quais
pedidos deram prejuízo. Eu não sabia.

O cliente paga, a nota é emitida, o pedido vai embora. O valor que a transportadora
vai cobrar de verdade só aparece na fatura, dias ou semanas depois. Quando o produto é
pequeno e leve, sobra. Quando é grande, pesado ou vai pra ponta do país, perde.

E a média mensal esconde isso. A planilha de vendas dizia que eu estava ganhando. A
fatura da transportadora dizia o contrário.

O que faltava era juntar os dois lados. Hoje é uma planilha que funciona como banco,
com um Apps Script alimentando ela todo dia:

Uma aba com uma linha por nota emitida, puxada de todas as contas do ERP.
Uma aba com uma linha por lançamento de transportadora, puxada da API do agregador.
As transportadoras que ficam fora do agregador entram manual.

O casamento é por número da nota mais transportadora. A diferença entre o que foi
cobrado do cliente e o que a transportadora cobrou vira uma coluna: sobra ou prejuízo,
pedido a pedido.

O que mudou na prática não foi a planilha, foi o que dá pra fazer com ela. Renegociar
tabela com transportadora deixou de ser conversa de feeling e passou a ter número por
região. Preço de produto pesado e de longa distância foi ajustado com base no custo
real. Cobrança extra de excedente de peso e taxa de devolução pararam de passar
batidas.

Um aviso que eu daria pra mim mesma no começo: fiz o casamento na mão, no Excel, antes
de escrever qualquer código. Foi assim que descobri os casos chatos — nota cancelada,
devolução, transportadora fora do agregador. Automatizar antes de entender o processo
só acelera o caos.

O detalhe da estrutura está em nak.api.br/cases/fretes-consolidado
```

---

## Post 5 — Impressão automática de separação

*Publicar 13/10/2026 · aponta pra `/cases/motoboy-impressao`*

```
Como imprimir a separação de pedido do Tiny ERP automaticamente.

Motoboy não espera. Ele chega, pega o pacote e sai. Se a separação não está pronta,
ou ele fica parado no balcão, ou vai embora e volta depois. Motoboy parado custa duas
vezes: paga ele e atrasa o próximo cliente.

Antes, alguém da equipe precisava ficar olhando o ERP pra ver se entrou pedido de
entrega rápida, imprimir e separar. Quando a equipe estava ocupada com outra coisa, o
pedido escapava.

A peça técnica é boba: um script Python que roda no mesmo PC ligado à impressora
térmica. Ele consulta o ERP de tempos em tempos atrás de separação aguardando com
aquela forma de envio, imprime, atualiza o status e manda um aviso no Slack.

Três decisões que valeram mais que o código:

Consulta em intervalo, não webhook. Webhook é mais elegante. Mas consulta local é à
prova de bala: se a internet cai, ele tenta de novo no ciclo seguinte, sem perder
pedido. Não tem servidor no meio.

Estado em arquivo JSON local, sem banco. Dois arquivos guardam o que já foi
processado e o que já foi impresso. Resolve duplicidade sem nenhuma infraestrutura.

Janela de horário. Fora do expediente ele não fica gastando chamada de API à toa.

Depois de um tempo em produção, o que mais melhorou não foi a impressão em si. Foi uma
tela web simples de reimpressão. Papel trava na térmica, alguém pega o cupom errado, e
antes disso a reimpressão era um comando no terminal com o número da nota. Ninguém da
expedição vai fazer isso. Hoje é buscar por cliente ou data e clicar.

Pagamento aprovado vira pedido saindo em até 10 minutos, com zero clique humano no
meio. Custo único foi a impressora térmica — nenhuma mensalidade.

O ganho real foi tirar uma pergunta da cabeça da equipe: "tem alguma coisa pra
imprimir agora?".

O fluxo completo está em nak.api.br/cases/motoboy-impressao
```

---

## Post 6 — Coletor de código de barras

*Publicar 27/10/2026 · aponta pra `/cases/romaneio-scanner`*

```
Alternativa barata a coletor de código de barras pra conferir romaneio de coleta.

Coletor de código de barras é caro e vem amarrado a um sistema. Aqui o coletor virou o
celular que a pessoa já tem no bolso, e o sistema é uma página web aberta no
navegador. Nada pra instalar, nada pra configurar quando entra aparelho novo.

O problema que originou isso: a transportadora leva os volumes e vai embora. Semanas
depois aparece a cobrança de um pacote que "não chegou". Sem romaneio conferido, quem
tem que provar que o pacote saiu é sempre a gente.

A conferência era no papel, no olho, com o motorista esperando. O conferente erra, o
motorista tem pressa e o papel some.

A leitura usa o detector de código de barras nativo do navegador, com uma biblioteca
de reserva quando o aparelho não tem. Tem lanterna pro galpão escuro e vibração
diferente pro bipe certo e pro erro, porque na expedição ninguém fica olhando a tela.

A parte que fez isso servir pra todas as transportadoras, e não só pra quem exigiu o
romaneio: o próprio formato do código diz qual é a transportadora. Nove padrões
cobrem o que passa pela expedição, e a classificação acontece no ato do bipe. Ninguém
escolhe transportadora numa lista antes.

Dois padrões existem só pra evitar lixo na lista. Código de 44 dígitos é chave de
nota fiscal, e o sistema recusa o bipe avisando — é o erro mais comum de quem está
começando, porque o código é grande e chama atenção. E código que não bate com padrão
nenhum só entra se a pessoa bipar de novo, confirmando.

O erro que me ensinou mais: a primeira versão consultava o ERP a cada bipe pra
descobrir o pedido e a nota. Funcionava perfeitamente na minha mesa, um volume por
vez. Na expedição, com o motorista esperando, cada bipe ficava parado esperando
resposta HTTP e a fila engasgava. A correção foi inverter — um sincronismo em segundo
plano guarda a relação rastreio, pedido e nota num cache, e o bipe faz busca local. O
dado na tela pode estar alguns minutos velho. Na prática não muda nada, e a fila anda.

Um clique fecha o dia: agrupa por transportadora, publica no Slack e trava a lista.
Divergência virou consulta, não discussão.

Zero hardware, zero licença. Está em nak.api.br/cases/romaneio-scanner
```

---

## O que medir depois

30 dias após o primeiro post, rodar os 6 prompts fixos e anotar linha nova na tabela
GEO do `SEO_BASELINE.md`. Olhar também o referral de `chatgpt.com`, `perplexity.ai` e
`claude.ai` no Cloudflare Web Analytics.

Ressalva honesta pra não gerar expectativa errada: com um post o efeito esperado é
nenhum. O que move citação em LLM é repetição ao longo de meses. O primeiro post serve
pra sair do zero absoluto de menções, que é uma condição diferente de "poucas menções".
