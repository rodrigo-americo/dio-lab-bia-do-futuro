# 🤖 CarreiraTron — Assistente Virtual de Carreira e Estudos em Tecnologia

Projeto do Lab da DIO **"Construa Seu Assistente Virtual Com Inteligência Artificial"**.
Fork do [repositório base](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro),
adaptado do exemplo financeiro para o tema de **orientação de carreira e estudos**.

---

## O que é

O **CarreiraTron** é um assistente de conversa (CLI) que ajuda uma pessoa **iniciante ou em
transição de carreira** a dar o próximo passo rumo a uma vaga em tecnologia:

- **Escolher uma trilha** (front-end, back-end, dados, QA, infra) com base nos interesses e
  no tempo que ela tem;
- **Montar um plano de estudos semanal realista** (modelos de 5 a 20 h/semana);
- **Preparar os próximos passos**: portfólio, primeira entrevista e dúvidas frequentes
  (faculdade, CLT x PJ, inglês, certificações).

Ele responde **apenas com base na base de conhecimento** em [`data/`](./data/), **cita a
fonte** de cada resposta e, quando não tem a informação, **diz que não sabe** — não inventa
curso, link, prazo ou salário.

**Para quem serve:** quem está migrando de outra área para tecnologia, estudantes ainda sem
foco definido e autodidatas sem mentor. Perfil de referência dos testes: `Sam` (atendimento,
~10 h/semana, gosta de lógica e de padrões).

---

## Como rodar

Requisito: [`uv`](https://docs.astral.sh/uv/) instalado ([instruções](https://docs.astral.sh/uv/getting-started/installation/)).

```bash
# 1. instalar as dependências (uv cria o .venv sozinho)
uv sync

# 2a. MODO NORMAL — usa a API da OpenAI (precisa de chave)
cp .env.example .env          # edite e preencha OPENAI_API_KEY
uv run python src/app.py

# 2b. MODO SIMULADO — sem chave e sem internet (mostra os trechos da base)
uv run python src/app.py --mock

# 2c. uma pergunta só e sai
uv run python src/app.py --ask "Preciso de faculdade para ser dev?"
```

Dentro do chat, digite `sair` para encerrar. O modelo padrão é `gpt-4o-mini`
(barato); dá para trocar com a variável `OPENAI_MODEL`.

### Exemplos de conversa

| Pergunta | O que o agente faz |
|----------|--------------------|
| "Gosto de achar padrões e não curto design. Tenho 10h/semana. Qual trilha?" | Sugere **Dados**, cita `trilhas.json`, encaixa o plano de 10h e dá um próximo passo |
| "Já decidi back-end e só tenho 5 horas por semana. Como divido esse tempo?" | Usa o modelo de rotina de **5h** de `planos_estudo.csv` |
| "Quanto ganha um dev júnior em São Paulo?" | **Não inventa** — diz que não tem essa informação e aponta onde procurar |
| "Qual a previsão do tempo amanhã?" | Responde que está **fora do escopo** |

---

## Como os 6 passos do desafio foram cumpridos

| Passo | Entrega | Onde |
|-------|---------|------|
| 1. Documentação do Agente | Caso de uso, persona, arquitetura (diagrama Mermaid), estratégias anti-alucinação | [`docs/01-documentacao-agente.md`](./docs/01-documentacao-agente.md) |
| 2. Base de Conhecimento | 5 arquivos em `data/` (trilhas, recursos, planos, FAQ, perfil) + estratégia de integração e limitações | [`docs/02-base-conhecimento.md`](./docs/02-base-conhecimento.md) · [`data/`](./data/) |
| 3. Prompts do Agente | System prompt final + racional, template de mensagem, few-shot e edge cases | [`docs/03-prompts.md`](./docs/03-prompts.md) · [`src/prompts/system_prompt.txt`](./src/prompts/system_prompt.txt) |
| 4. Aplicação Funcional | CLI em Python com retrieval por palavra-chave + API OpenAI + modo `--mock` | [`src/`](./src/) |
| 5. Avaliação e Métricas | Roteiro de 10 testes, métricas (assertividade, segurança, aderência, utilidade) e feedback de pessoas | [`docs/04-metricas.md`](./docs/04-metricas.md) |
| 6. Pitch | Roteiro de ~3 min para gravação em vídeo + checklist | [`docs/05-pitch.md`](./docs/05-pitch.md) |

🎥 **Vídeo do pitch:** _(a gravar — link será adicionado aqui e em `docs/05-pitch.md`)_

---

## Estrutura do repositório

```
desafio_dio/  (fork de dio-lab-bia-do-futuro)
├── README.md                     # este arquivo
├── pyproject.toml / uv.lock      # dependências (uv): openai, python-dotenv
├── .env.example                  # modelo — a chave real fica só no .env (git-ignorado)
│
├── data/                         # base de conhecimento (dados fictícios)
│   ├── trilhas.json              # trilhas de carreira e habilidades
│   ├── cursos_recursos.json      # tipos de recurso de estudo por trilha/nível
│   ├── planos_estudo.csv         # rotinas semanais por horas disponíveis
│   ├── faq_carreira.md           # perguntas frequentes (com id por item)
│   └── perfil_usuario_exemplo.json  # persona fictícia "Sam" para os testes
│
├── docs/                         # documentação dos 6 passos (01 a 05)
│
├── src/
│   ├── app.py                    # CLI: loop de conversa no terminal
│   ├── agent.py                  # monta o prompt e chama a IA (ou o mock)
│   ├── knowledge_base.py         # carrega data/ e faz o retrieval
│   └── prompts/system_prompt.txt # instruções de comportamento do agente
│
├── assets/                       # espaço para diagramas e screenshots
└── examples/                     # referências do repositório base
```

---

## Limitações (por decisão de projeto)

Protótipo simples, não produção:

- Base de conhecimento pequena (5 trilhas, ~13 recursos, 11 FAQs) e com dados fictícios.
- Retrieval por **palavra-chave**, sem embeddings — pode trazer um trecho irrelevante no
  contexto de vez em quando (o system prompt mitiga isso na resposta final).
- Sem dados dinâmicos: nada de vagas reais, salários ou datas de curso.
- Perfil da pessoa é fixo (arquivo de exemplo), não preenchido em conversa.

Próximos passos possíveis estão listados em [`docs/04-metricas.md`](./docs/04-metricas.md).

---

## Créditos

Desafio **DIO** — [Lab: Construa Seu Assistente Virtual Com Inteligência Artificial](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro).
Estrutura de pastas e templates de `docs/` vêm do repositório base; a base de conhecimento,
os prompts, a aplicação e a avaliação são deste projeto.
