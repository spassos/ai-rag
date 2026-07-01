"""Motor de consulta: recupera contexto, gera resposta e cita as fontes.

No PoC offline usamos retrieval ``naive`` (vetorial sobre os chunks) com
``only_need_context``, para não depender de um LLM real na etapa de recuperação.
A resposta final é produzida pelo provedor (``generate``) e as citações são
extraídas do contexto recuperado — garantindo a fundamentação (Constituição P1).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from lightrag import LightRAG, QueryParam

from ..providers.base import BaseProvider

_FONTE = re.compile(r"Fonte:\s*([^\s\"}\\]+)")


@dataclass
class Answer:
    """Resposta fundamentada a uma pergunta."""

    question: str
    answer: str
    citations: list[str] = field(default_factory=list)
    context: str = ""

    @property
    def grounded(self) -> bool:
        """True se a resposta tem ao menos uma fonte (RF4)."""
        return bool(self.citations)


class QueryEngine:
    def __init__(self, rag: LightRAG, provider: BaseProvider, top_k: int = 5) -> None:
        self.rag = rag
        self.provider = provider
        self.top_k = top_k

    async def answer(self, question: str) -> Answer:
        context = await self.rag.aquery(
            question,
            param=QueryParam(
                mode="naive",
                only_need_context=True,
                top_k=self.top_k,
                enable_rerank=False,
            ),
        )
        context = context or ""
        citations = self._extract_citations(context)
        if not citations:
            return Answer(
                question=question,
                answer="Não há dados suficientes no acervo para responder a esta pergunta.",
                citations=[],
                context=context,
            )
        texto = await self.provider.generate(question, context)
        return Answer(question=question, answer=texto, citations=citations, context=context)

    @staticmethod
    def _extract_citations(context: str) -> list[str]:
        vistos: list[str] = []
        for url in _FONTE.findall(context.replace("\\n", "\n")):
            url = url.strip().rstrip('",}')
            if url and url not in vistos:
                vistos.append(url)
        return vistos
