"""Carrega a base de conhecimento (pasta data/) e faz uma recuperação simples por
palavra-chave. Sem embeddings nem banco vetorial — o objetivo é um protótipo claro.

Cada "documento" recuperável é um trecho de texto com um rótulo de origem
(ex.: "trilhas.json / dados") para o agente poder citar a fonte.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Palavras muito comuns que não ajudam a diferenciar um trecho do outro.
_STOPWORDS = {
    "a", "o", "os", "as", "de", "da", "do", "das", "dos", "e", "ou", "um", "uma",
    "que", "com", "sem", "para", "pra", "por", "em", "no", "na", "nos", "nas",
    "meu", "minha", "eu", "me", "se", "qual", "quais", "quanto", "quanta", "como",
    "quero", "gosto", "tenho", "sou", "estou", "ser", "estar", "mais", "menos",
    "isso", "esse", "essa", "sobre", "ao", "aos", "the",
}


def _normalize(text: str) -> str:
    """minúsculas + remoção de acentos, para casar 'código' com 'codigo'."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower()


_NUM_EXTENSO = {
    "uma": "1", "duas": "2", "tres": "3", "quatro": "4", "cinco": "5",
    "seis": "6", "sete": "7", "oito": "8", "nove": "9", "dez": "10",
    "doze": "12", "quinze": "15", "vinte": "20",
}


def _tokens(text: str) -> set[str]:
    norm = _normalize(text)
    words = re.findall(r"[a-z0-9]+", norm)
    toks = {w for w in words if len(w) > 2 and w not in _STOPWORDS}
    # Normaliza referências a horas/semana para o token "<n>h", para casar com o
    # rótulo do CSV de planos: "5h", "5 horas", "cinco horas por semana"...
    norm_num = norm
    for extenso, digito in _NUM_EXTENSO.items():
        norm_num = re.sub(rf"\b{extenso}\b", digito, norm_num)
    for n in re.findall(r"(\d{1,2})\s*h(?:oras?)?\b", norm_num):
        toks.add(f"{n}h")
    return toks


@dataclass
class Doc:
    source: str          # rótulo de origem, ex. "trilhas.json / dados"
    text: str            # texto do trecho
    _tokens: set[str]

    _source_tokens: set[str]

    @classmethod
    def make(cls, source: str, text: str) -> "Doc":
        return cls(
            source=source,
            text=text.strip(),
            _tokens=_tokens(source + " " + text),
            _source_tokens=_tokens(source),
        )

    def score(self, query_tokens: set[str]) -> int:
        # Palavra que casa com o rótulo da fonte (ex.: "back-end") pesa o dobro.
        base = len(self._tokens & query_tokens)
        boost = len(self._source_tokens & query_tokens)
        # Um token de horas ("5h", "10h"...) no rótulo é um sinal muito específico
        # (é o identificador de uma linha do planos_estudo.csv): peso extra.
        hour_hit = len({t for t in self._source_tokens & query_tokens if t.endswith("h") and t[:-1].isdigit()})
        return base + boost + 2 * hour_hit


class KnowledgeBase:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.docs: list[Doc] = []
        self.profile_text: str = "não informado"
        self._load()

    # ----- carregamento -----------------------------------------------------
    def _load(self) -> None:
        self._load_trilhas()
        self._load_cursos()
        self._load_planos()
        self._load_faq()
        self._load_perfil()

    def _read_json(self, name: str):
        return json.loads((self.data_dir / name).read_text(encoding="utf-8"))

    def _load_trilhas(self) -> None:
        data = self._read_json("trilhas.json")
        for t in data.get("trilhas", []):
            text = (
                f"{t['nome']} — {t['resumo']}\n"
                f"Combina com: {t['combina_com']}\n"
                f"Pré-requisitos: {', '.join(t['pre_requisitos'])}\n"
                f"Habilidades-chave: {', '.join(t['habilidades_chave'])}\n"
                f"Não é sobre: {', '.join(t.get('nao_e_sobre', []))}\n"
                f"Tempo estimado de fundamentos: {t['tempo_estimado_fundamentos_horas']} h\n"
                f"Primeiros passos: {' | '.join(t['primeiros_passos'])}"
            )
            self.docs.append(Doc.make(f"trilhas.json / {t['id']}", text))

    def _load_cursos(self) -> None:
        data = self._read_json("cursos_recursos.json")
        for r in data.get("recursos", []):
            text = (
                f"Recurso de estudo — trilha {r['trilha']}, nível {r['nivel']}.\n"
                f"Tema: {r['tema']}\n"
                f"Formato: {r['formato']}\n"
                f"Carga horária estimada: {r['carga_horaria_estimada_horas']} h\n"
                f"Objetivo: {r['objetivo']}\n"
                f"Critério de conclusão: {r['criterio_conclusao']}"
            )
            self.docs.append(
                Doc.make(f"cursos_recursos.json / {r['trilha']}-{r['nivel']}-{r['tema']}", text)
            )

    def _load_planos(self) -> None:
        with (self.data_dir / "planos_estudo.csv").open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                text = (
                    f"Plano para {row['horas_por_semana']} h/semana ({row['perfil_tempo']}).\n"
                    f"Dias sugeridos: {row['dias_sugeridos']}\n"
                    f"Bloco por dia: {row['bloco_por_dia_min']} min\n"
                    f"Distribuição: {row['distribuicao']}\n"
                    f"Ritmo esperado: {row['ritmo_esperado']}\n"
                    f"Observação: {row['observacao']}"
                )
                self.docs.append(
                    Doc.make(f"planos_estudo.csv / {row['horas_por_semana']}h", text)
                )

    def _load_faq(self) -> None:
        raw = (self.data_dir / "faq_carreira.md").read_text(encoding="utf-8")
        # Cada item começa com "## <id>" seguido de "**pergunta**" e a resposta.
        for block in re.split(r"\n##\s+", raw):
            block = block.strip()
            m = re.match(r"(faq-[\w-]+)\s*\n+(.*)", block, flags=re.DOTALL)
            if not m:
                continue
            faq_id, body = m.group(1), m.group(2).strip()
            self.docs.append(Doc.make(f"faq_carreira.md / {faq_id}", body))

    def _load_perfil(self) -> None:
        data = self._read_json("perfil_usuario_exemplo.json")
        p = data.get("perfil", {})
        conhecimento = "; ".join(f"{k}: {v}" for k, v in p.get("conhecimento_atual", {}).items())
        self.profile_text = (
            f"{p.get('nome_ficticio', 'Pessoa')} — {p.get('situacao_atual', '')}.\n"
            f"Objetivo: {p.get('objetivo', '')}\n"
            f"Interesses: {', '.join(p.get('interesses', []))}\n"
            f"Aversões: {', '.join(p.get('aversao', []))}\n"
            f"Tempo disponível: {p.get('tempo_disponivel_semana_horas', '?')} h/semana\n"
            f"Conhecimento atual: {conhecimento}\n"
            f"Restrições: {', '.join(p.get('restricoes', []))}\n"
            f"Observação: {p.get('observacao_para_o_agente', '')}"
        )

    # ----- recuperação ----------------------------------------------------
    def search(self, query: str, limit: int = 4, min_score: int = 2) -> list[Doc]:
        """Retorna os trechos com mais palavras-chave em comum com a pergunta.

        `min_score` é o mínimo de palavras em comum para um trecho contar. Com 1,
        qualquer coincidência solta (ex.: "tempo" de "previsão do tempo" casando com
        "tempo estimado") traria lixo; 2 reduz esses falsos positivos. Se nada
        alcançar o piso, cai para 1 antes de desistir.
        """
        q = _tokens(query)
        if not q:
            return []
        scored = sorted(
            ((d.score(q), d) for d in self.docs),
            key=lambda pair: pair[0],
            reverse=True,
        )
        hits = [d for s, d in scored if s >= min_score]
        # Fallback para score 1 só quando a pergunta é curta (1-2 palavras úteis).
        # Numa pergunta longa, um único termo em comum quase sempre é ruído.
        if not hits and len(q) <= 2:
            hits = [d for s, d in scored if s >= 1]
        return hits[:limit]

    def build_context(self, query: str, limit: int = 4) -> tuple[str, list[str]]:
        """Monta o bloco CONTEXTO e devolve também a lista de fontes usadas."""
        hits = self.search(query, limit=limit)
        if not hits:
            return ("(nenhum trecho da base de conhecimento casou com esta pergunta)", [])
        parts = [f"[{d.source}]\n{d.text}" for d in hits]
        return ("\n\n".join(parts), [d.source for d in hits])
