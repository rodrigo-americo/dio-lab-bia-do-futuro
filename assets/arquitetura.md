# Arquitetura do CarreiraTron

Diagrama do fluxo de uma pergunta, do terminal até a resposta.

```mermaid
flowchart TD
    A[Pessoa usuária] -->|Pergunta no terminal| B[app.py<br/>CLI]
    B --> G[knowledge_base.py<br/>carrega e busca em data/]
    G -->|Trechos relevantes + fonte + perfil| B
    B -->|CONTEXTO + PERFIL + PERGUNTA| C[agent.py]
    C -->|modo normal| D[API OpenAI<br/>gpt-4o-mini · temperature 0.2]
    C -->|modo --mock| E[Fallback local<br/>mostra os trechos da base]
    D --> F[Resposta ancorada na base]
    E --> F
    F --> A

    H[(data/<br/>trilhas · cursos_recursos<br/>planos_estudo · faq_carreira · perfil)] --- G
    I[[src/prompts/system_prompt.txt]] --- C
```

## Componentes

| Componente | Arquivo | Papel |
|------------|---------|-------|
| Interface | `src/app.py` | Loop de conversa no terminal; flags `--mock` e `--ask` |
| Recuperação | `src/knowledge_base.py` | Lê `data/`, quebra em trechos com rótulo de origem, busca por palavra-chave (com peso extra para o rótulo da fonte) |
| Orquestração / Prompt | `src/agent.py` | Monta `CONTEXTO + PERFIL + PERGUNTA` e aplica o system prompt |
| LLM | OpenAI `gpt-4o-mini` | Gera a resposta (só no modo normal) |
| Base de conhecimento | `data/*.json`, `data/*.csv`, `data/*.md` | Fonte única de verdade do agente |
| Anti-alucinação | `src/prompts/system_prompt.txt` | Regras: responder só pelo contexto, citar fonte, admitir quando não sabe |

> Screenshots da aplicação em execução podem ser adicionados aqui para o README e o pitch.
