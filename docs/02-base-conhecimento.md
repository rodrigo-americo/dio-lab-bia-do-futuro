# Base de Conhecimento

A base de conhecimento do **CarreiraTron** é pequena de propósito: cinco arquivos em
[`../data/`](../data/), todos com dados **fictícios e genéricos**, criados para o Lab DIO.
Eles substituem os arquivos do exemplo financeiro do repositório base.

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|----------------------|
| [`trilhas.json`](../data/trilhas.json) | JSON | Descrever cada trilha de carreira (front-end, back-end, dados, QA, infra/DevOps): resumo, com quem combina, pré-requisitos, habilidades-chave, o que **não** é, tempo estimado e primeiros passos. Base para a recomendação de trilha. |
| [`cursos_recursos.json`](../data/cursos_recursos.json) | JSON | Listar **tipos** de recurso de estudo por trilha e nível (fundamentos/intermediário), com tema, formato, carga horária estimada e critério de conclusão. O agente recomenda o tema e o tipo, nunca um nome/link específico. |
| [`planos_estudo.csv`](../data/planos_estudo.csv) | CSV | Modelos de rotina semanal por horas disponíveis (5, 8, 10, 15, 20 h/semana): dias sugeridos, duração do bloco, distribuição entre teoria/prática/revisão e ritmo esperado. Base para o plano de estudos. |
| [`faq_carreira.md`](../data/faq_carreira.md) | Markdown | Perguntas frequentes com resposta curta e honesta (faculdade, portfólio, tempo até a primeira vaga, CLT x PJ, inglês, certificações, entrevista...). Cada item tem um `id` para o agente citar como fonte. |
| [`perfil_usuario_exemplo.json`](../data/perfil_usuario_exemplo.json) | JSON | Persona fictícia (`Sam`) usada para manter as conversas de teste consistentes: situação atual, objetivo, interesses, tempo disponível, conhecimento atual e restrições. |

> As duas interfaces (web `src/web.py` e CLI `src/app.py`) usam exatamente esta mesma
> estratégia — só muda a forma de mostrar a resposta.

## Estratégia de integração

1. **Carregamento:** a aplicação lê os cinco arquivos de `data/` uma vez, no início da sessão.
2. **Recuperação (retrieval simples):** a cada pergunta, o app procura por palavras-chave da
   pergunta nos arquivos e seleciona os trechos mais relevantes (itens de trilha, linhas do
   CSV, entradas da FAQ). Não há embeddings nem banco vetorial — é busca textual direta.
3. **Montagem do contexto:** os trechos selecionados são colados num bloco `CONTEXTO`, seguido
   do `PERFIL` (quando disponível) e da `PERGUNTA`. O detalhe do template está em
   [`03-prompts.md`](./03-prompts.md).
4. **Uso pelo modelo:** o system prompt obriga o agente a responder **apenas** com o que está
   no `CONTEXTO` e a citar o arquivo/`id` de origem. Se o retrieval não trouxe nada útil, o
   agente deve dizer que não sabe.

## Exemplo de Contexto Montado

Pergunta da pessoa: *"Gosto de achar padrões e não curto design. Tenho 10h por semana. Qual trilha?"*

```
CONTEXTO (base de conhecimento — use apenas isto):

[trilhas.json / id: dados]
Dados (análise e engenharia de dados) — Coletar, organizar e analisar dados para apoiar decisões.
Combina com: quem gosta de estatística, de encontrar padrões e de contar histórias com números.
Pré-requisitos: lógica de programação básica; matemática do ensino médio.
Habilidades-chave: Python para dados (pandas); SQL; visualização; estatística descritiva.
Primeiros passos: aprender SQL num banco de exemplo; aprender pandas com um CSV público;
montar um painel simples.

[trilhas.json / id: front-end]
Front-end — combina com quem gosta de layout e de resultado visual rápido. (menos aderente
ao interesse declarado)

[planos_estudo.csv / linha: 10 h/semana]
perfil_tempo: moderado; dias_sugeridos: 4 a 5 dias; bloco_por_dia_min: 75;
distribuicao: 2 dias de conteúdo novo + 2 dias de projeto + 1 dia de revisão;
ritmo_esperado: fundamentos em ~3 meses.

PERFIL DA PESSOA:
Sam — trabalha com atendimento, sem experiência em programação. Objetivo: primeira vaga em
tecnologia em ~1 ano. Interesses: lógica, organização, padrões. Pouco interesse em design.
Tempo: 10 h/semana.

PERGUNTA DA PESSOA:
Gosto de achar padrões e não curto design. Tenho 10h por semana. Qual trilha?
```

## Limitações e próximos passos

- **Base pequena:** cinco trilhas, ~13 recursos, 11 itens de FAQ. Cobre o essencial de uma
  conversa de orientação, mas não substitui pesquisa de mercado atualizada.
- **Dados fictícios:** carga horária e prazos são estimativas genéricas, não medições reais.
- **Retrieval por palavra-chave:** pode não achar sinônimos (ex.: "programar" vs. "codar").
  Próximo passo natural seria busca semântica com embeddings.
- **Sem dados dinâmicos:** nada de vagas reais, salários ou datas de curso — isso é decisão
  de projeto, para manter o protótipo simples e seguro.
- **Evolução possível:** ampliar a FAQ, adicionar mais trilhas (ex.: mobile, segurança,
  UX research) e permitir que a pessoa preencha o próprio perfil em vez de usar o de exemplo.
