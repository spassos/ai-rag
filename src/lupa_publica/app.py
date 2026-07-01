"""Orquestração do pipeline: normaliza → indexa → consulta.

Função única reutilizada pela CLI (comando ``smoke``) e pelos testes, garantindo
que o caminho exercitado no sandbox é o mesmo do CI (Constituição P9).
"""

from __future__ import annotations

from .config import Settings
from .index.builder import create_rag, index_registros
from .ingest.normalize import normalize_contrato
from .providers.factory import get_provider
from .query.engine import Answer, QueryEngine


async def run_pipeline(
    settings: Settings, raw_contratos: list[dict], question: str
) -> Answer:
    """Executa o fluxo completo sobre uma lista de contratos brutos."""
    provider = get_provider(settings)
    registros = [normalize_contrato(r, settings.transparencia_base_url) for r in raw_contratos]

    rag = await create_rag(settings, provider)
    try:
        await index_registros(rag, registros)
        engine = QueryEngine(rag, provider, top_k=settings.top_k)
        return await engine.answer(question)
    finally:
        await rag.finalize_storages()
