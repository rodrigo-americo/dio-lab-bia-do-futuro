# Código da Aplicação — CarreiraTron

Protótipo de linha de comando (CLI) do assistente. Feito em Python, com recuperação simples
sobre a base de conhecimento em [`../data/`](../data/) e resposta via API da OpenAI.

## Arquivos

```
src/
├── web.py              # interface web (Streamlit) — recomendada para a demo
├── app.py              # interface de linha de comando (CLI)
├── agent.py            # monta o prompt (CONTEXTO + PERFIL + PERGUNTA) e chama a IA (ou o mock)
├── knowledge_base.py   # carrega data/ e faz a busca por palavra-chave (retrieval)
└── prompts/
    └── system_prompt.txt   # instruções de comportamento do agente
```

`web.py` e `app.py` são só camadas de interface — toda a lógica está em
`agent.py` + `knowledge_base.py`.

## Dependências

Gerenciadas com [`uv`](https://docs.astral.sh/uv/) na raiz do projeto
(`../pyproject.toml` + `../uv.lock`): `openai`, `python-dotenv` e `streamlit`.

## Como rodar

Na **raiz do projeto**:

```bash
# 1. instalar as dependências (cria o .venv automaticamente)
uv sync

# 2. chave da OpenAI (só para o modo normal)
cp .env.example .env      # e preencha OPENAI_API_KEY
```

### Interface web

```bash
uv run streamlit run src/web.py
```

Tela de chat no navegador. Botão **Modo simulado** na barra lateral para rodar sem chave.

### Linha de comando

```bash
uv run python src/app.py                 # modo normal (precisa da chave)
uv run python src/app.py --mock          # modo simulado, sem chave nem internet
uv run python src/app.py --ask "Preciso de faculdade para ser dev?"   # pergunta única
```

Dentro do chat da CLI, digite `sair` para encerrar.

## Como funciona (resumo)

1. `knowledge_base.py` lê os 5 arquivos de `data/` e transforma cada item em um "trecho"
   com rótulo de origem (ex.: `trilhas.json / dados`).
2. A cada pergunta, ele seleciona os trechos com mais palavras-chave em comum.
3. `agent.py` monta a mensagem para o modelo e aplica o `system_prompt.txt`, que obriga o
   agente a responder **só** com o que está no contexto e a citar a fonte.
4. `gpt-4o-mini` responde com `temperature` baixa. No modo `--mock`, nada é enviado à rede.
