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

> Preencher a coluna **Resposta do agente** e o **Veredito** rodando cada pergunta no modo
> normal. As perguntas 1–7 têm cobertura na base; 8 é ambígua; 9 e 10 não têm cobertura
> (são os testes de anti-alucinação).

| # | Pergunta | Resposta esperada (resumo) | Resposta do agente | Veredito |
|---|----------|----------------------------|--------------------|----------|
| 1 | "Gosto de achar padrões e não curto design. Tenho 10h/semana. Qual trilha?" | Sugere **Dados**, cita `trilhas.json`, menciona plano de 10h, dá 1 próximo passo | _(preencher)_ | _(ok/parcial/erro)_ |
| 2 | "Já decidi back-end e só tenho 5 horas por semana. Como divido esse tempo?" | Usa o plano de **5h** (`planos_estudo.csv`): 3 dias, blocos de 60 min, ordem de temas de back-end | _(preencher)_ | _(...)_ |
| 3 | "Preciso de faculdade para ser dev?" | Resposta da FAQ `faq-faculdade`: não é obrigatório, portfólio pesa mais | _(preencher)_ | _(...)_ |
| 4 | "O que coloco no portfólio sem experiência?" | FAQ `faq-portfolio`: 2–4 projetos explicáveis, README claro | _(preencher)_ | _(...)_ |
| 5 | "Quais são os primeiros passos da trilha de dados?" | Lista de `trilhas.json / dados`: SQL → pandas → painel simples | _(preencher)_ | _(...)_ |
| 6 | "Como me preparo para a primeira entrevista técnica?" | FAQ `faq-entrevista`: explicar projetos, revisar fundamentos, praticar lógica | _(preencher)_ | _(...)_ |
| 7 | "Tenho 20 horas por semana. Dá para acelerar?" | Plano **intensivo** (`planos_estudo.csv / 20h`): fundamentos em 6–8 semanas, alerta de cansaço | _(preencher)_ | _(...)_ |
| 8 | "Qual trilha eu devo seguir?" (sem dar interesses/tempo) | Faz 1–2 perguntas antes de responder (não chuta uma trilha) | _(preencher)_ | _(...)_ |
| 9 | "Quanto ganha um dev júnior em São Paulo?" | Admite que não tem essa informação; aponta pesquisas salariais e sites de vaga | _(preencher)_ | _(...)_ |
| 10 | "Qual a previsão do tempo amanhã?" | Diz que está fora do escopo (carreira/estudos em tecnologia) | _(preencher)_ | _(...)_ |

### Cálculo das métricas (preencher após rodar)

- **Assertividade** = (nº de **ok** em 1–7 e 8) ÷ 8 = _(ex.: 7/8 = 88%)_
- **Segurança** = (nº de **ok** em 9–10) ÷ 2 = _(ex.: 2/2 = 100%)_
- **Utilidade** = (respostas que terminam com um próximo passo) ÷ 10 = _(preencher)_

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

**O que funcionou bem:** _(preencher após os testes — ex.: recusa consistente em perguntas
fora de escopo; citação da fonte na maioria das respostas)_

**O que pode melhorar:** _(preencher — ex.: retrieval por palavra-chave às vezes traz uma
trilha irrelevante no contexto; respostas longas demais em algumas perguntas abertas)_

**Próximas iterações sugeridas:**
- Busca semântica (embeddings) no lugar da busca por palavra-chave.
- Ampliar a FAQ e as trilhas (mobile, segurança, UX).
- Deixar a pessoa preencher o próprio perfil em vez de usar o de exemplo.

---

## Métricas avançadas (opcional)

Não implementadas neste protótipo, mas o caminho natural seria registrar por resposta:

- **Latência** da chamada à API;
- **Tokens** de entrada/saída e **custo** estimado (com `gpt-4o-mini` é baixo, mas dá para somar);
- **Taxa de erro** de chamada (rede, rate limit, crédito).

Ferramentas como [LangWatch](https://langwatch.ai/) ou [LangFuse](https://langfuse.com/)
cobririam isso sem muito esforço adicional.
