"""CarreiraTron — interface web (Streamlit).

Roda com:
    uv run streamlit run src/web.py

Requisitos:
- modo normal: OPENAI_API_KEY no arquivo .env (copie de .env.example)
- modo simulado: nenhuma chave necessária — marque "Modo simulado" na barra lateral

A lógica é a mesma da CLI (src/app.py): esta tela só chama o Agent.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Permite importar os módulos de src/ mesmo com o Streamlit rodando da raiz.
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:  # dotenv é opcional para o modo simulado
    pass

from agent import Agent  # noqa: E402
from knowledge_base import KnowledgeBase  # noqa: E402

EXEMPLOS = [
    "Gosto de achar padrões e não curto design. Tenho 10h por semana. Qual trilha?",
    "Já decidi back-end e só tenho 5 horas por semana. Como divido esse tempo?",
    "Preciso de faculdade para conseguir a primeira vaga como dev?",
]

st.set_page_config(page_title="CarreiraTron", page_icon="🤖")


@st.cache_resource(show_spinner=False)
def carregar_base() -> KnowledgeBase:
    return KnowledgeBase()


@st.cache_resource(show_spinner=False)
def carregar_agente(mock: bool) -> Agent | str:
    """Devolve o Agent pronto, ou uma string de erro se faltar a chave."""
    try:
        return Agent(carregar_base(), mock=mock)
    except RuntimeError as exc:
        return str(exc)


# ---- Barra lateral --------------------------------------------------------
st.sidebar.title("CarreiraTron")
st.sidebar.caption("Mentor de carreira e estudos em tecnologia")
modo_mock = st.sidebar.toggle(
    "Modo simulado (sem API)",
    value=False,
    help="Não chama a OpenAI. Mostra os trechos da base de conhecimento.",
)
st.sidebar.divider()
st.sidebar.markdown("**Exemplos de perguntas**")
for ex in EXEMPLOS:
    st.sidebar.markdown(f"- {ex}")
if st.sidebar.button("Limpar conversa"):
    st.session_state.pop("mensagens", None)
    st.rerun()

# ---- Área principal -----------------------------------------------------
st.title("🤖 CarreiraTron")
st.write(
    "Assistente que ajuda quem está começando ou migrando para tecnologia a escolher "
    "uma trilha, montar um plano de estudos e se preparar para as primeiras vagas. "
    "Responde com base na pasta `data/` e diz quando não sabe."
)

agente = carregar_agente(modo_mock)
if isinstance(agente, str):  # erro (ex.: sem OPENAI_API_KEY)
    st.error(agente)
    st.info("Marque **Modo simulado** na barra lateral para usar sem chave de API.")
    st.stop()

if modo_mock:
    st.warning("Modo simulado ativo — as respostas não passam pela IA.", icon="🧪")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("fontes"):
            st.caption("Fontes: " + ", ".join(msg["fontes"]))

pergunta = st.chat_input("Sua dúvida sobre carreira ou estudos em tecnologia...")
if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando a base e pensando..."):
            resposta, fontes = agente.answer_with_sources(pergunta)
        st.markdown(resposta)
        if fontes:
            st.caption("Fontes: " + ", ".join(fontes))

    st.session_state.mensagens.append(
        {"role": "assistant", "content": resposta, "fontes": fontes}
    )
