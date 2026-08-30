# Plano — Lab DIO: Construa Seu Assistente Virtual Com Inteligência Artificial

**Tema escolhido:** Orientação de carreira e estudos (adaptação do exemplo "Edu, Educador Financeiro").
**Nome do assistente:** *CarreiraTron* — mentor de carreira e plano de estudos em tecnologia.
  (nome provisório; alternativas discutidas: Bússola, Trilha, Rumo, Norte, Farol, Guru Júnior, PlanoCerto)
**Idioma dos entregáveis:** português (pt-BR).
**Gerência de dependências (Passo 4):** `uv` (não `requirements.txt` solto) — `pyproject.toml` + `uv.lock`.
**Entrega:** Fork do repositório base `digitalinnovationone/dio-lab-bia-do-futuro`.
**Repositório base:** https://github.com/digitalinnovationone/dio-lab-bia-do-futuro

> Objetivo do lab: protótipo simples, funcional e bem explicado que mostra como a IA
> apoia uma pessoa numa tarefa real, usando uma base de conhecimento e evitando
> respostas inventadas.

---

## 0. Ideia do assistente (resumo de 3 linhas)

*CarreiraTron* ajuda uma pessoa que está começando ou migrando para a área de tecnologia a:
1. entender qual trilha de aprendizado combina com o objetivo dela (front-end, back-end, dados, QA...);
2. montar um plano de estudos semanal realista a partir do tempo disponível;
3. preparar os próximos passos (portfólio, currículo, primeira entrevista).

Quando não houver informação suficiente na base de conhecimento, o assistente diz
que não sabe e sugere onde a pessoa pode buscar — nunca inventa cursos, links ou prazos.

---

## 1. Preparação do repositório (antes dos 6 passos)

| Passo | Ação |
|-------|------|
| 1.1 | Fazer **Fork** de `digitalinnovationone/dio-lab-bia-do-futuro` na conta do GitHub (usuário: rodrigo_7_4_7@hotmail.com). |
| 1.2 | `git clone` do fork para uma pasta local (pode ser esta: `c:\Users\Aluno\Desktop\desafio_dio`). |
| 1.3 | Criar branch de trabalho: `git checkout -b entrega/carreiratron`. |
| 1.4 | Conferir a estrutura que já vem no fork: `README.md`, `data/`, `docs/`, `src/`, `assets/`, `examples/`. |
| 1.5 | Ler os templates em `docs/01..05` e os exemplos em `examples/` — eles são o esqueleto a preencher. |
| 1.6 | Substituir o `README.md` do fork pelo README do nosso projeto (ver passo 7). |

**Estrutura-alvo final** (adaptada da estrutura do repo base):

```
dio-lab-bia-do-futuro/  (nosso fork)
├── README.md                     # apresentação do projeto CarreiraTron
├── pyproject.toml                # projeto + dependências (uv)
├── uv.lock                       # lockfile gerado pelo uv
├── .env.example                  # OPENAI_API_KEY=  (a chave real fica só no .env local)
├── .gitignore                    # .env, .venv/, __pycache__/, *.pyc
├── data/                         # base de conhecimento
│   ├── trilhas.json              # trilhas de carreira e habilidades
│   ├── cursos_recursos.json      # cursos/recursos de estudo (mockados)
│   ├── planos_estudo.csv         # modelos de plano semanal por carga horária
│   ├── faq_carreira.md           # perguntas frequentes (portfólio, CLT/PJ, júnior)
│   └── perfil_usuario_exemplo.json  # perfil fictício para os testes
├── docs/
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   └── 05-pitch.md
├── src/
│   ├── app.py                    # loop de conversa no terminal
│   ├── knowledge_base.py         # carrega data/ e faz o retrieval simples
│   ├── agent.py                  # monta o prompt e chama a API da OpenAI (ou --mock)
│   └── prompts/system_prompt.txt
└── assets/
    └── arquitetura.md / arquitetura.png  (diagrama Mermaid)
```

---

## 2. Passo 1 — Documentação do Agente  → `docs/01-documentacao-agente.md`

Preencher com **escolhas próprias**, não texto genérico:

- **Caso de uso:** que problema o CarreiraTron resolve (pessoa perdida sobre por onde começar
  em tecnologia; excesso de conteúdo solto; falta de plano realista).
- **Para quem serve:** iniciante em transição de carreira / estudante de curso técnico
  ou superior / autodidata sem mentor.
- **Persona e tom de voz:** encorajador, direto, sem jargão desnecessário, foca em um
  próximo passo por vez. Nunca promete emprego nem prazos garantidos.
- **O que ele NÃO faz:** não indica vagas específicas, não dá consultoria jurídica/salarial
  precisa, não substitui mentor humano.
- **Arquitetura (diagrama Mermaid):** usuário → pergunta → app carrega base de conhecimento
  (`data/`) → monta prompt (system + contexto + pergunta) → LLM → resposta → usuário.
- **Segurança / anti-alucinação:** regra "responda só com base no CONTEXTO fornecido;
  se não estiver lá, diga que não sabe"; citar de qual arquivo da base veio a informação.

**Saída do passo:** documento preenchido + `assets/arquitetura` com o diagrama.

---

## 3. Passo 2 — Base de Conhecimento  → `data/` + `docs/02-base-conhecimento.md`

Começar **pequena** e adaptar os dados do repo base ao tema de carreira.

| Arquivo | Formato | Conteúdo (mockado, ~5–15 itens) |
|---------|---------|--------------------------------|
| `trilhas.json` | JSON | Ex.: Front-end, Back-end, Dados, QA — para cada: descrição, pré-requisitos, habilidades-chave, perfil que combina. |
| `cursos_recursos.json` | JSON | Recursos de estudo fictícios/genéricos por trilha e nível (fundamentos, intermediário), com carga horária estimada. |
| `planos_estudo.csv` | CSV | Modelos de plano semanal por horas/semana disponíveis (ex.: 5h, 10h, 20h) → distribuição por dia/tema. |
| `faq_carreira.md` | Markdown | Perguntas frequentes: "preciso de faculdade?", "o que colocar no portfólio?", "quanto tempo até a primeira vaga?", "CLT ou PJ?". Respostas curtas e honestas. |
| `perfil_usuario_exemplo.json` | JSON | Persona fictícia (objetivo, tempo disponível, conhecimento atual) usada nos testes de forma consistente. |

`docs/02-base-conhecimento.md` deve explicar: **por que** esses dados, **como** estão
organizados, **como** o app os usa, e as **limitações** (base pequena, dados fictícios).

**Saída do passo:** 5 arquivos em `data/` + documento explicando a estratégia de dados.

---

## 4. Passo 3 — Prompts do Agente  → `docs/03-prompts.md` (+ arquivo usável)

- **System Prompt** (versão final + racional de cada regra):
  - papel do assistente e público;
  - "use SOMENTE o CONTEXTO abaixo; se faltar informação, diga que não sabe e sugira
    onde procurar";
  - formato de resposta (curta, 1 próximo passo, cita a fonte da base);
  - proibições (não inventar cursos/links/prazos, não prometer emprego).
- **Template de mensagem** enviada ao LLM: `system` + `CONTEXTO` (trechos da base) +
  `PERGUNTA DO USUÁRIO` + `PERFIL` (opcional).
- **Exemplos de interação** (3–5): entrada → saída esperada. Incluir 1 caso em que a
  resposta correta é "não tenho essa informação".
- **Edge cases:** pergunta fora do escopo (ex.: receita de bolo), pergunta ambígua,
  pergunta sensível (salário exato numa cidade), base sem cobertura.
- Salvar o system prompt também como arquivo reaproveitável (`src/prompts/system_prompt.txt`),
  para colar em qualquer chat de IA e para o `agent.py` carregar.

**Saída do passo:** `docs/03-prompts.md` completo + system prompt em arquivo.

---

## 5. Passo 4 — Aplicação Funcional  → `src/`

> **DECIDIDO:** Python CLI + **API da OpenAI** (você já tem créditos), com RAG simples
> (busca por palavra-chave na base `data/`, injeta os trechos no prompt).
> Modelo sugerido: `gpt-4o-mini` (barato e suficiente para o protótipo).

Estrutura de código (ver mapa completo na seção 1):

```
pyproject.toml            # projeto + deps (uv) — dependências: openai, python-dotenv
uv.lock                   # lockfile do uv (commitado)
.env.example              # OPENAI_API_KEY=
src/
├── app.py                # loop de conversa no terminal (aceita --mock)
├── knowledge_base.py     # carrega data/ e faz a busca simples (retrieval)
├── agent.py              # monta o prompt e chama a API da OpenAI
└── prompts/system_prompt.txt
```

Setup com **uv** (substitui `requirements.txt` + venv manual):
- `uv init` (ou criar o `pyproject.toml` à mão) e `uv add openai python-dotenv`;
- rodar: `uv run python src/app.py`  (o uv cria/gerencia o `.venv` sozinho);
- `uv.lock` vai pro Git; `.venv/` não;
- no README, instrução de execução em 2 linhas: `uv sync` depois `uv run python src/app.py`.

Detalhes da integração OpenAI:
- SDK novo (`openai` v1+): `from openai import OpenAI; client = OpenAI()`;
- ler a chave de `OPENAI_API_KEY` via `python-dotenv` (arquivo `.env` **fora** do Git);
- chamada: `client.chat.completions.create(model="gpt-4o-mini", messages=[...])`
  com `messages = [{"role":"system", ...}, {"role":"user", <contexto + pergunta>}]`;
- `temperature` baixa (0–0.3) e `max_tokens` moderado para reduzir alucinação e custo;
- tratar erro de rede / falta de chave / crédito esgotado com mensagem clara.

Requisitos do protótipo:
- roda com um comando (`uv run python src/app.py`);
- 3+ perguntas de exemplo documentadas no README;
- código **comentado** e simples;
- trata o caso "não sei" de forma visível (quando a base não cobre a pergunta);
- **modo offline** (`uv run python src/app.py --mock`): sem chave, cai num fallback que só
  mostra os trechos da base — garante que a aplicação "roda" mesmo sem crédito na avaliação.

**Saída do passo:** app que conversa no terminal + `pyproject.toml` + `uv.lock` + `.env.example` + instruções.
**Ação necessária de você:** ter o `uv` instalado e a `OPENAI_API_KEY` num `.env` local na hora de testar.

---

## 6. Passo 5 — Avaliação e Métricas  → `docs/04-metricas.md`

- **Cenários de teste** (tabela com ~8–10 linhas): pergunta | resposta esperada |
  resposta do agente | veredito (ok / parcial / erro) | observação.
  Incluir: perguntas dentro do escopo, 1 ambígua, 1 fora do escopo, 1 sem cobertura na base.
- **Métricas** (adaptadas das sugeridas pelo repo base):
  - *Assertividade* = respostas corretas / total;
  - *Taxa de resposta segura* = % de vezes que NÃO alucinou (quando não sabia, admitiu);
  - *Aderência ao perfil* = respostas coerentes com o `perfil_usuario_exemplo.json`;
  - *Utilidade* = a resposta dá um próximo passo claro? (sim/não).
- **Análise:** o que funcionou, o que falhou, e 2–3 melhorias futuras
  (base maior, retrieval melhor, mais exemplos no prompt).

**Saída do passo:** documento com a tabela de testes preenchida e a leitura das métricas.

---

## 7. Passo 6 — Pitch  → `docs/05-pitch.md`

Roteiro de **~3 minutos** (estilo elevador):
1. **Problema** (30s): pessoa querendo entrar em tecnologia se perde na quantidade de
   conteúdo e não tem plano.
2. **Solução** (45s): o que o CarreiraTron faz e como usa a base de conhecimento.
3. **Demonstração** (60s): 1–2 perguntas reais + a resposta (print ou fala), incluindo
   o caso "não sei".
4. **Diferencial / valor** (30s): respostas honestas e ancoradas na base, foco em um
   próximo passo, fácil de evoluir.
5. **Aprendizados** (15s): o que você tirou do processo.

**Você vai gravar o vídeo.** Checklist da gravação:
- roteiro escrito antes (o de cima), cronometrado para não passar de ~3 min;
- gravar a tela mostrando o `uv run python src/app.py` respondendo 1–2 perguntas de verdade,
  incluindo o caso "não sei";
- áudio limpo; pode ser OBS Studio, Loom ou a própria gravação de tela do Windows (Win+G);
- subir no YouTube (não listado) ou Drive e colocar o link no `docs/05-pitch.md` e no `README.md`.

**Saída do passo:** roteiro escrito (e, se quiser, link do vídeo/slides).

---

## 8. README.md do projeto (raiz do fork)

Deve apresentar: nome e objetivo do CarreiraTron; para quem serve; como está organizado
(mapa das pastas); **como os 6 passos foram cumpridos** (links para cada `docs/0X`);
como rodar a aplicação (`uv sync` → `uv run python src/app.py`, com e sem `--mock`);
exemplos de conversa; limitações e próximos passos; link do vídeo do pitch;
créditos (Lab DIO + link do repo base).

---

## 9. Fechamento e entrega

| Passo | Ação |
|-------|------|
| 9.1 | Revisar todos os `docs/` e o `README.md`. |
| 9.2 | `git add . && git commit` em mensagens pequenas por etapa. |
| 9.3 | `git push` da branch para o fork. |
| 9.4 | Abrir Pull Request no próprio fork (ou manter na branch `main` do fork), conforme a orientação da atividade na plataforma DIO. |
| 9.5 | Submeter o link do repositório na plataforma da DIO. |
| 9.6 | (Portfólio) Fixar o repo no perfil do GitHub e escrever um post/resumo. |

---

## 10. Ordem de execução sugerida

1. Fork + clone + branch (Passo 1).
2. **Prompts** primeiro (Passo 3) — dica nº 1 do repo base: o system prompt é a base.
3. **Base de conhecimento** (Passo 2) — em paralelo com o prompt.
4. **Documentação do agente** (Passo 1) — já dá para escrever com prompt + base prontos.
5. **Aplicação funcional** (Passo 4) — Python CLI + OpenAI + modo `--mock`.
6. **Avaliação e métricas** (Passo 5) — rodar os testes no app.
7. **Pitch** (Passo 6, com vídeo) e **README** — por último, com tudo pronto.

---

## 11. Decisões — status

| # | Decisão | Status |
|---|---------|--------|
| 1 | Tema: orientação de carreira e estudos em tecnologia | **DECIDIDO** |
| 2 | Nome: **CarreiraTron** (provisório; alternativas: Bússola, Trilha, Rumo, Norte, Farol) | provisório — pode trocar |
| 3 | Passo 4: **Python CLI + API OpenAI** (`gpt-4o-mini`), deps via **`uv`**, modo `--mock` de reserva | **DECIDIDO** |
| 4 | Idioma dos entregáveis: **português (pt-BR)** | **DECIDIDO** |
| 5 | Pitch: **vídeo gravado** + roteiro | **DECIDIDO** |

---

## 12. Pontos de atenção (com a escolha da OpenAI)

1. **Segurança da chave (crítico).** A `OPENAI_API_KEY` vai num `.env` local que **nunca**
   é commitado. Adicionar ao `.gitignore`: `.env`, `__pycache__/`, `.venv/`, `*.pyc`.
   Versionar só o `.env.example` com a chave em branco.
2. **Custo.** `gpt-4o-mini` é barato, mas cada rodada de teste consome crédito.
   Usar `max_tokens` moderado, `temperature` baixa e não deixar loop de teste rodando à toa.
3. **A aplicação precisa "rodar" na avaliação mesmo sem crédito/internet.** Por isso o
   **modo `--mock`**: sem chave válida, o app responde só com os trechos da base + aviso.
   Documentar os dois modos no README.
4. **Anti-alucinação continua sendo o foco do lab.** O system prompt deve forçar
   "responda só com base no CONTEXTO; se não estiver lá, diga que não sabe". Isso vale
   pontos na avaliação e nas métricas (taxa de resposta segura).
5. **Não expor dados reais.** Tudo em `data/` é fictício (perfil de usuário, cursos,
   recursos). Nada de dados pessoais seus ou de terceiros.
6. **Dependências via `uv`**: `pyproject.toml` + `uv.lock` commitados; deps mínimas
   (`openai`, `python-dotenv`). Antes de entregar, rodar `uv sync` num clone limpo
   para garantir que instala e `uv run python src/app.py` executa do zero.
   No README, exigir o `uv` instalado (link para a doc oficial de instalação).
7. **Escopo pequeno de propósito.** Base de conhecimento com 5–15 itens por arquivo;
   retrieval por palavra-chave (sem embeddings/vetores) — o lab pede protótipo simples,
   não produção. Registrar isso como "limitação e próximo passo" nos docs.
8. **Compatibilidade do SDK.** Usar a API nova do SDK `openai` (v1+):
   `from openai import OpenAI; client = OpenAI()`. O `uv.lock` fixa a versão exata,
   então o corretor pega o mesmo SDK que você testou.
9. **README como vitrine.** É o que o avaliador (e recrutador) lê primeiro: mapa das
   pastas, como rodar (com e sem chave), exemplos de conversa, link do vídeo, os 6 passos
   com link para cada `docs/0X`.
10. **Fluxo Git da DIO.** Fork → commits pequenos por etapa → push → seguir a instrução
    da plataforma (geralmente PR no próprio fork ou entrega do link do repo).
