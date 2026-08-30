"""CarreiraTron — aplicação de linha de comando (Lab DIO).

Uso:
    uv run python src/app.py            # modo normal, precisa de OPENAI_API_KEY no .env
    uv run python src/app.py --mock     # modo simulado, sem chamar a API
    uv run python src/app.py --ask "sua pergunta"   # uma pergunta só e sai

Comandos dentro do chat: 'sair' ou 'exit' encerram.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# No terminal do Windows a saída padrão costuma ser cp1252 e quebra os acentos.
# Forçar UTF-8 deixa a conversa (e a gravação do pitch) legível.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):  # ambiente sem suporte a reconfigure
        pass

# Permite rodar tanto "python src/app.py" quanto "python app.py".
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent import Agent  # noqa: E402
from knowledge_base import KnowledgeBase  # noqa: E402

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # dotenv é opcional para o modo --mock
    pass

BANNER = r"""
  ____                 _         _____
 / ___|__ _ _ __ _ __ (_)_ _ __|_   _| __ ___  _ __
| |   / _` | '__| '__|| | '__/ _ \| || '__/ _ \| '_ \
| |__| (_| | |  | |   | | | |  __/| || | | (_) | | | |
 \____\__,_|_|  |_|   |_|_|  \___||_||_|  \___/|_| |_|

CarreiraTron — mentor de carreira e estudos em tecnologia
"""

EXEMPLOS = [
    "Gosto de achar padrões e não curto design. Tenho 10h por semana. Qual trilha?",
    "Já decidi back-end e só tenho 5 horas por semana. Como divido esse tempo?",
    "Preciso de faculdade para conseguir a primeira vaga como dev?",
]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CarreiraTron CLI")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="modo simulado: não chama a API, só mostra os trechos da base",
    )
    parser.add_argument(
        "--ask",
        metavar="PERGUNTA",
        help="faz uma única pergunta, imprime a resposta e encerra",
    )
    return parser.parse_args(argv)


def run() -> None:
    args = parse_args(sys.argv[1:])

    kb = KnowledgeBase()
    try:
        agent = Agent(kb, mock=args.mock)
    except RuntimeError as exc:
        print(f"\n{exc}\n")
        sys.exit(1)

    if args.ask:
        print(agent.answer(args.ask))
        return

    print(BANNER)
    if args.mock:
        print("(rodando em modo simulado — sem chamar a IA)\n")
    print("Exemplos de perguntas:")
    for ex in EXEMPLOS:
        print(f"  - {ex}")
    print("\nDigite 'sair' para encerrar.\n")

    while True:
        try:
            question = input("você > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not question:
            continue
        if question.lower() in {"sair", "exit", "quit"}:
            break
        print()
        print(f"CarreiraTron > {agent.answer(question)}")
        print()

    print("Até a próxima. Bons estudos!")


if __name__ == "__main__":
    run()
