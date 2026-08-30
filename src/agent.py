"""Monta o prompt e obtém a resposta do CarreiraTron.

Dois modos:
- normal: chama a API da OpenAI (modelo gpt-4o-mini por padrão).
- mock:   não usa rede; devolve os trechos da base de conhecimento com um aviso.
          Serve para rodar o protótipo sem chave de API / sem crédito.
"""

from __future__ import annotations

import os
from pathlib import Path

from knowledge_base import KnowledgeBase

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "system_prompt.txt"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


def build_user_message(kb: KnowledgeBase, question: str) -> tuple[str, list[str]]:
    context, sources = kb.build_context(question)
    message = (
        "CONTEXTO (base de conhecimento — use apenas isto):\n"
        f"{context}\n\n"
        "PERFIL DA PESSOA (quando disponível):\n"
        f"{kb.profile_text}\n\n"
        "PERGUNTA DA PESSOA:\n"
        f"{question}"
    )
    return message, sources


class Agent:
    def __init__(self, kb: KnowledgeBase, *, mock: bool = False, model: str = DEFAULT_MODEL):
        self.kb = kb
        self.mock = mock
        self.model = model
        self.system_prompt = load_system_prompt()
        self._client = None
        if not self.mock:
            self._client = self._make_client()

    def _make_client(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY não encontrada. Crie um arquivo .env a partir de "
                ".env.example ou rode em modo simulado: --mock"
            )
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "Pacote 'openai' não instalado. Rode 'uv sync' antes de usar."
            ) from exc
        return OpenAI(api_key=api_key)

    def answer(self, question: str) -> str:
        user_message, sources = build_user_message(self.kb, question)

        if self.mock:
            return self._mock_answer(sources, user_message)

        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                temperature=0.2,
                max_tokens=500,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            return resp.choices[0].message.content.strip()
        except Exception as exc:  # rede, crédito, chave inválida, etc.
            return (
                "Não consegui falar com a API da OpenAI agora "
                f"({exc.__class__.__name__}: {exc}).\n"
                "Você pode tentar de novo ou rodar em modo simulado com --mock."
            )

    def _mock_answer(self, sources: list[str], user_message: str) -> str:
        if not sources:
            return (
                "[modo simulado] Não encontrei nada na base de conhecimento para esta "
                "pergunta. Num cenário real, eu diria que não tenho essa informação e "
                "sugeriria procurar em sites de vagas, pesquisas salariais do setor ou "
                "comunidades da área."
            )
        trechos = user_message.split("PERFIL DA PESSOA")[0]
        return (
            "[modo simulado — sem chamar a IA]\n"
            "Estes são os trechos da base de conhecimento mais relevantes para a sua "
            "pergunta. No modo normal, o CarreiraTron usaria só este conteúdo para "
            "responder de forma curta e com um próximo passo.\n\n"
            f"{trechos.strip()}\n\n"
            f"Fontes: {', '.join(sources)}"
        )
