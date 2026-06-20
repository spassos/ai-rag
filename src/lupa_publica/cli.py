"""CLI da Lupa Pública.

Comandos:
- ``smoke``: roda o pipeline completo offline sobre uma fixture e valida que a
  resposta vem com citação de fonte. É o teste local do sandbox (Constituição P9).
- ``query``: indexa uma fixture e responde a uma pergunta informada.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import tempfile
from pathlib import Path

from .app import run_pipeline
from .config import Settings
from .ingest.client import load_fixture
from .query.engine import Answer

_DEFAULT_FIXTURE = (
    Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "contratos_sample.json"
)


def _print_answer(ans: Answer) -> None:
    print("\n=== RESPOSTA ===")
    print(ans.answer)
    print("\n=== FONTES ===")
    for url in ans.citations:
        print(f"- {url}")
    if not ans.citations:
        print("(nenhuma fonte — resposta não fundamentada)")


def _cmd_query(args: argparse.Namespace) -> int:
    raw = load_fixture(args.fixture)
    with tempfile.TemporaryDirectory() as tmp:
        settings = Settings.from_env()
        settings = Settings(
            provider=settings.provider,
            working_dir=str(Path(tmp) / "rag"),
            top_k=settings.top_k,
            cosine_threshold=settings.cosine_threshold,
            transparencia_base_url=settings.transparencia_base_url,
        )
        ans = asyncio.run(run_pipeline(settings, raw, args.question))
    _print_answer(ans)
    return 0 if ans.grounded else 1


def _cmd_smoke(args: argparse.Namespace) -> int:
    question = args.question or "contratos de seringas para a saúde"
    print(f"[smoke] provider=fake (offline) | fixture={args.fixture}")
    raw = load_fixture(args.fixture)
    with tempfile.TemporaryDirectory() as tmp:
        settings = Settings(provider="fake", working_dir=str(Path(tmp) / "rag"))
        ans = asyncio.run(run_pipeline(settings, raw, question))
    _print_answer(ans)
    ok = ans.grounded
    print(f"\n[smoke] resultado: {'OK ✅' if ok else 'FALHOU ❌ (sem fonte)'}")
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lupa-publica", description="RAG de gastos públicos.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_smoke = sub.add_parser("smoke", help="Teste local offline (Constituição P9).")
    p_smoke.add_argument("--fixture", default=str(_DEFAULT_FIXTURE))
    p_smoke.add_argument("--question", default=None)
    p_smoke.set_defaults(func=_cmd_smoke)

    p_query = sub.add_parser("query", help="Indexa uma fixture e responde uma pergunta.")
    p_query.add_argument("question")
    p_query.add_argument("--fixture", default=str(_DEFAULT_FIXTURE))
    p_query.set_defaults(func=_cmd_query)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
