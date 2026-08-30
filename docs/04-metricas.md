# Avaliação e Métricas

## Como avaliei o CarreiraTron

Duas formas complementares:

1. **Testes estruturados** — um roteiro fixo de 10 perguntas com resposta esperada, rodado
   no app. Cada resposta recebe um veredito: **ok**, **parcial** ou **erro**.
2. **Feedback de pessoas** — de 3 a 5 pessoas conversam livremente com o agente e dão nota
   de 1 a 5 para cada métrica. Antes, recebem o contexto do perfil fictício `Sam`
   (ver [`../data/perfil_usuario_exemplo.json`](../data/perfil_usuario_exemplo.json)).

> **Como reproduzir os testes estruturados**
> ```bash
> uv run python src/app.py --ask "..."      # uma pergunta por vez, modo normal (com a chave)
> uv run python src/app.py --mock --ask "..."   # para conferir só o retrieval, sem a IA
> ```

---

## Métricas de qualidade

| Métrica | O que avalia | Como medi |
|---------|--------------|-----------|
| **Assertividade** | O agente respondeu o que foi perguntado, de acordo com a base? | respostas **ok** ÷ total de testes |
| **Segurança (anti-alucinação)** | Quando não tinha a informação, o agente admitiu em vez de inventar? | testes sem cobertura respondidos com "não sei" ÷ testes sem cobertura |
| **Aderência ao perfil** | A resposta faz sentido para o perfil `Sam` (interesses, 10 h/semana)? | avaliação 1–5 por pessoa, média |
| **Utilidade** | A resposta terminou com um próximo passo concreto e pequeno? | sim ÷ total |

---

## Roteiro de testes estruturados

> Rodado em **2026-08-29** contra o modo normal (`gpt-4o-mini`, `temperature` 0.2), com o
> perfil `Sam` no contexto. As perguntas 1–7 têm cobertura na base; 8 é ambígua; 9 e 10 não
> têm cobertura (são os testes de anti-alucinação). As respostas completas estão no fim
> deste documento.

| # | Pergunta | Resposta esperada (resumo) | Resposta do agente (resumo) | Veredito |
|---|----------|----------------------------|-----------------------------|----------|
| 1 | "Gosto de achar padrões e não curto design. Tenho 10h/semana. Qual trilha?" | Sugere **Dados**, cita `trilhas.json`, menciona plano de 10h, dá 1 próximo passo | Sugeriu Dados; citou pré-requisitos, habilidades e "130h" da base; encaixou o plano de 10h; próximo passo (começar SQL e pandas). | **ok** |
| 2 | "Já decidi back-end e só tenho 5 horas por semana. Como divido esse tempo?" | Usa o plano de **5h** (`planos_estudo.csv`): 3 dias, blocos de 60 min, ordem de temas de back-end | **1ª rodada:** o retrieval não trouxe o `planos_estudo.csv / 5h` (a pessoa escreveu "5 horas", não "5h") e o modelo inventou a divisão "2h + 1,5h + 1,5h" → **parcial**. **Após a correção do tokenizador** (reconhecer "N horas" e números por extenso + peso extra para o token de horas no rótulo): retrieval passou a trazer o plano de 5h e a resposta ficou ancorada — "3 dias na semana, blocos de 60 min, 2 dias de conteúdo novo + 1 dia de prática, ~5 a 6 meses" → **ok**. | **parcial → ok** (após ajuste) |
| 3 | "Preciso de faculdade para ser dev?" | Resposta da FAQ `faq-faculdade`: não é obrigatório, portfólio pesa mais | Fiel à FAQ, citou `faq-faculdade`, fechou com próximo passo. | **ok** |
| 4 | "O que coloco no portfólio sem experiência?" | FAQ `faq-portfolio`: 2–4 projetos explicáveis, README claro | Fiel à FAQ (2–4 projetos, explicar problema/decisões/aprendizado, README claro); próximo passo. | **ok** |
| 5 | "Quais são os primeiros passos da trilha de dados?" | Lista de `trilhas.json / dados`: SQL → pandas → painel simples | Exatamente os 3 passos da base, na ordem; próximo passo. Retrieval trouxe outras trilhas no contexto, mas a resposta não se contaminou. | **ok** |
| 6 | "Como me preparo para a primeira entrevista técnica?" | FAQ `faq-entrevista`: explicar projetos, revisar fundamentos, praticar lógica | Cobriu todos os pontos da FAQ, incluindo a entrevista comportamental; próximo passo. | **ok** |
| 7 | "Tenho 20 horas por semana. Dá para acelerar?" | Plano **intensivo** (`planos_estudo.csv / 20h`): fundamentos em 6–8 semanas, alerta de cansaço | Usou o plano de 20h da base (5–6 dias, blocos de 120 min, 6–8 semanas) e repetiu o alerta de cansaço/sono; próximo passo. | **ok** |
| 8 | "Qual trilha eu devo seguir?" (sem dar interesses/tempo) | Faz 1–2 perguntas antes de responder (não chuta uma trilha) | Respondeu direto com 3 trilhas (Dados, Software, QA) usando o perfil `Sam` que estava no contexto — **não fez a pergunta que o system prompt pede**. Também citou "Excel", que não está na base. Ofereceu montar o plano como próximo passo. | **parcial** |
| 9 | "Quanto ganha um dev júnior em São Paulo?" | Admite que não tem essa informação; aponta pesquisas salariais e sites de vaga | Recusou corretamente ("não tenho informações sobre faixas salariais") e indicou onde procurar. Citou LinkedIn/Glassdoor de conhecimento próprio (exemplos genéricos, não vieram da base). | **ok** |
| 10 | "Qual a previsão do tempo amanhã?" | Diz que está fora do escopo (carreira/estudos em tecnologia) | Recusou por fora de escopo e redirecionou para carreira, apesar de o retrieval ter trazido um trecho irrelevante (`faq-tempo-primeira-vaga`, por causa da palavra "tempo"). O prompt segurou. | **ok** |

### Resultado das métricas (rodada de 2026-08-29)

Considerando a rodada final (com a correção do tokenizador aplicada entre a 1ª e a 2ª rodada):

- **Assertividade** = **ok** em 1, 2, 3, 4, 5, 6, 7 e **parcial** em 8 → **7/8 pleno (≈88%)**,
  ou **≈94%** contando o parcial como meio ponto.
  - Antes do ajuste no retrieval, o teste 2 também era parcial (6/8 pleno).
- **Segurança (anti-alucinação)** = testes 9 e 10 → **2/2 = 100%**. Em nenhum teste o agente
  inventou um dado factual da base (curso, prazo, salário). O único desvio remanescente (#8)
  foi citar "Excel" como exemplo genérico, não uma afirmação falsa.
- **Utilidade** = **10/10** — todas as respostas terminaram com um próximo passo concreto.

---

## Feedback de pessoas (1–5)

| Participante | Assertividade | Aderência ao perfil | Utilidade | Comentário |
|--------------|:-------------:|:-------------------:|:---------:|------------|
| P1 | | | | |
| P2 | | | | |
| P3 | | | | |
| **Média** | | | | |

> Lembrete: contextualizar cada participante sobre o perfil fictício `Sam` antes do teste.

---

## Resultados

**O que funcionou bem:**
- **Anti-alucinação sólida:** nos dois testes sem cobertura (9 e 10) o agente admitiu a
  lacuna e redirecionou, mesmo quando o retrieval entregou um trecho irrelevante no contexto
  (#10). Nenhuma resposta inventou um dado factual da base.
- **Fidelidade à FAQ:** perguntas 3, 4 e 6 saíram praticamente coladas às entradas da FAQ,
  com citação da fonte.
- **Uso dos planos de estudo:** #1 e #7 encaixaram corretamente a linha certa do
  `planos_estudo.csv` (10h e 20h) e repetiram os alertas da base.
- **Utilidade:** 10/10 respostas terminaram com um próximo passo pequeno e concreto.

**O que pode melhorar:**
- ~~Retrieval falha em casar o `planos_estudo.csv` quando a pessoa escreve "5 horas" em vez
  de "5h" (#2).~~ **Corrigido nesta rodada:** o tokenizador passou a normalizar "N horas" e
  números por extenso ("cinco horas") para o token `5h`, e esse token no rótulo de uma linha
  do CSV ganhou peso extra. O teste 2 subiu de parcial para ok.
- **Regra de "pergunte antes de responder" (#8) não dispara quando o perfil `Sam` já está
  no contexto** — o agente responde direto. Como no protótipo o perfil é sempre injetado,
  na prática essa regra quase nunca é exercida. Decidir: ou tornar o perfil opcional na
  conversa, ou ajustar o system prompt para ainda confirmar a trilha com a pessoa.
- **Pequenos "vazamentos" de conhecimento geral:** o agente citou "Excel" (#8) e
  "LinkedIn/Glassdoor" (#9), que não estão na base. São exemplos genéricos e inofensivos,
  mas contrariam a regra de responder só pelo contexto. Reforçar no system prompt.
- **Respostas um pouco longas** em perguntas abertas (#4, #6, #8) — poderiam ser mais enxutas.

**Próximas iterações sugeridas:**
- Melhorar o tokenizador do retrieval (números por extenso e "N horas") e, no médio prazo,
  trocar a busca por palavra-chave por busca semântica (embeddings).
- Ampliar a FAQ e as trilhas (mobile, segurança, UX).
- Deixar a pessoa preencher o próprio perfil em vez de usar o de exemplo.
- Apertar o system prompt contra vazamento de conhecimento geral e encurtar respostas.

---

## Métricas avançadas (opcional)

Não implementadas neste protótipo, mas o caminho natural seria registrar por resposta:

- **Latência** da chamada à API;
- **Tokens** de entrada/saída e **custo** estimado (com `gpt-4o-mini` é baixo, mas dá para somar);
- **Taxa de erro** de chamada (rede, rate limit, crédito).

Ferramentas como [LangWatch](https://langwatch.ai/) ou [LangFuse](https://langfuse.com/)
cobririam isso sem muito esforço adicional.

---

## Anexo — respostas completas da rodada de 2026-08-29

> Geradas por `gpt-4o-mini` (`temperature` 0.2) com o perfil `Sam` no contexto.
> "fontes recuperadas" = trechos que o retrieval por palavra-chave selecionou de `data/`.

### #1 — "Gosto de achar padrões e não curto design. Tenho 10h por semana. Qual trilha?"
*fontes: planos_estudo.csv/10h, trilhas.json/back-end, trilhas.json/dados, trilhas.json/infra-devops*

> Com base nos seus interesses e no tempo disponível, a trilha de **Dados (análise e engenharia de dados)** parece ser a mais adequada para você. Essa trilha envolve coletar, organizar e analisar dados, o que se alinha bem com sua curiosidade por dados e planilhas. Além disso, não exige habilidades de design visual, que você mencionou não gostar.
>
> - **Pré-requisitos**: Lógica de programação básica (que você já possui), matemática do ensino médio e vontade de trabalhar com planilhas e consultas.
> - **Habilidades-chave**: Python para dados (pandas), SQL, visualização de dados e comunicação de resultados.
> - **Tempo estimado de fundamentos**: 130 horas.
>
> Os primeiros passos incluem aprender SQL fazendo consultas em um banco de exemplo e aprender pandas limpando e resumindo um CSV público. Como você tem 10 horas por semana, sugiro seguir o plano de estudos para essa carga horária, que envolve 4 a 5 dias de estudo por semana, alternando entre teoria e prática.
>
> **Próximo passo**: Comece a explorar SQL e pandas. Você pode procurar por tutoriais gratuitos online para iniciar seu aprendizado.

### #2 — "Já decidi back-end e só tenho 5 horas por semana. Como divido esse tempo?"

**1ª rodada** *(fontes: trilhas.json/back-end, cursos_recursos.json/back-end-* × 3; sem o plano de 5h)*

> [...] 1. Linguagem de servidor - 2h/semana. 2. APIs REST - 1,5h/semana. 3. Banco de dados e SQL - 1,5h/semana. Total estimado: 115 horas, ~5 meses. [...]
> _Divisão "2h + 1,5h + 1,5h" e "~5 meses" não vinham da base._

**2ª rodada, após corrigir o tokenizador** *(fontes: planos_estudo.csv/5h, trilhas.json/back-end, cursos_recursos.json/back-end-fundamentos-* × 2)*

> Com 5 horas por semana, você pode seguir um plano de estudos enxuto e consistente:
> - **Dias sugeridos**: 3 dias na semana
> - **Bloco por dia**: 60 minutos
> - **Distribuição**: 2 dias de conteúdo novo + 1 dia de prática/revisão
> - **Tempo estimado**: fundamentos da trilha de back-end em cerca de 5 a 6 meses, priorizando a consistência.
>
> **Próximos passos**: 1. Escolha uma linguagem (Python ou Node.js). 2. Inicie com um curso de sintaxe e comece a resolver exercícios pequenos.
>
> _Agora ancorado em `planos_estudo.csv / 5h`._

### #3 — "Preciso de faculdade para ser dev?"
*fontes: faq_carreira.md/faq-faculdade*

> Não é obrigatório ter faculdade para trabalhar como desenvolvedor. Muitas vagas valorizam mais o portfólio e testes técnicos do que um diploma. A faculdade pode ajudar a entender fundamentos e pode ser mais valorizada em empresas tradicionais ou em áreas específicas, mas não é o único caminho para entrar na área de tecnologia (segundo faq-faculdade). [...] Um próximo passo seria explorar essas trilhas e ver qual delas se alinha mais com seus interesses.

### #4 — "O que coloco no portfólio sem experiência?"
*fontes: faq_carreira.md/faq-portfolio*

> Para montar um portfólio mesmo sem experiência, você pode incluir de 2 a 4 projetos que consiga explicar em detalhe. [...] Para cada projeto, explique: o problema que você estava tentando resolver; as decisões técnicas que tomou; o que você aprendeu. Certifique-se de que o README seja claro e bem estruturado — isso é mais importante do que ter muitos projetos. **Próximo passo**: pense em um problema que você gostaria de resolver e comece a esboçar um projeto.

### #5 — "Quais são os primeiros passos da trilha de dados?"
*fontes: trilhas.json/dados, trilhas.json/front-end, trilhas.json/back-end, trilhas.json/infra-devops*

> 1. **Aprender SQL**: comece fazendo consultas em um banco de exemplo. 2. **Aprender pandas**: pratique limpando e resumindo um CSV público. 3. **Montar um painel simples**: crie um gráfico que responda a uma pergunta de negócio. [...] **Próximo passo**: que tal começar a aprender SQL?

### #6 — "Como me preparo para a primeira entrevista técnica?"
*fontes: faq_carreira.md/faq-entrevista, faq-tempo-primeira-vaga, faq-linguagem-primeira*

> 1. **Explique seus projetos** [...] 2. **Revise fundamentos** da trilha (para dados: lógica, SQL, fundamentos de programação) [...] 3. **Pratique lógica** com exercícios cronometrados. 4. **Prepare perguntas** para a empresa. 5. **Entrevista comportamental** conta tanto quanto a técnica. Um próximo passo concreto seria começar a revisar os fundamentos da programação e SQL essa semana.

### #7 — "Tenho 20 horas por semana. Dá para acelerar?"
*fontes: planos_estudo.csv/20h*

> Sim, com 20 horas por semana você pode acelerar. O plano sugerido é intensivo e pode levar aos fundamentos em cerca de 6 a 8 semanas: 5 a 6 dias na semana, blocos de 120 minutos, 2–3 dias de conteúdo novo + 2 dias de projeto + 1 dia de revisão + tempo para comunidade. Monitore seu cansaço e a qualidade do sono. [...] Um próximo passo concreto seria pesquisar sobre trilhas de programação ou análise de dados que se encaixem no seu perfil.

### #8 — "Qual trilha eu devo seguir?"
*fontes: (nenhuma recuperada)*

> Sam, considerando seus interesses e o tempo disponível: 1. **Análise de Dados** [...] 2. **Desenvolvimento de Software (foco em lógica)** — aprender Python [...] 3. **Testes de Software (QA)** [...] **Próximo passo**: escolha uma dessas trilhas e eu posso te ajudar a montar um plano de estudos semanal!
>
> _Observação da avaliação: não fez a pergunta que o system prompt pede (respondeu direto
> usando o perfil do contexto) e mencionou "Excel", que não está na base._

### #9 — "Quanto ganha um dev júnior em São Paulo?"
*fontes: (nenhuma recuperada)*

> Não tenho informações sobre faixas salariais específicas por cidade ou empresa. Recomendo que você pesquise em sites de vagas, como LinkedIn ou Glassdoor, e também consulte comunidades de tecnologia. Um próximo passo concreto seria explorar as trilhas de aprendizado em tecnologia que podem se alinhar com seus interesses.

### #10 — "Qual a previsão do tempo amanhã?"
*fontes: faq_carreira.md/faq-tempo-primeira-vaga (irrelevante — casou pela palavra "tempo")*

> Desculpe, mas não posso ajudar com informações sobre a previsão do tempo. Meu foco é auxiliar você na transição de carreira para a área de tecnologia. Que tal começarmos a discutir suas opções de trilhas de aprendizado?
