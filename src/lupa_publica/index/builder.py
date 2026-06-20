"""Construção e alimentação do índice LightRAG (file-based)."""

from __future__ import annotations

from collections.abc import Iterable

from lightrag import LightRAG
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import EmbeddingFunc

from ..config import Settings
from ..ingest.normalize import Registro, registro_to_document
from ..providers.base import BaseProvider
from ..tokenizer import build_local_tokenizer


async def create_rag(settings: Settings, provider: BaseProvider) -> LightRAG:
    """Cria um LightRAG file-based pronto para inserir/consultar.

    Usa os backends padrão (NanoVectorDB + NetworkX + JSON) sob
    ``settings.working_dir`` e o tokenizer local (sem rede).
    """
    rag = LightRAG(
        working_dir=settings.working_dir,
        tokenizer=build_local_tokenizer(),
        embedding_func=EmbeddingFunc(
            embedding_dim=provider.embedding_dim,
            max_token_size=100_000,
            func=provider.embed,
        ),
        llm_model_func=provider.llm,
        entity_extract_max_gleaning=0,
        enable_llm_cache=False,
        cosine_better_than_threshold=settings.cosine_threshold,
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()
    return rag


async def index_registros(rag: LightRAG, registros: Iterable[Registro]) -> int:
    """Indexa registros canônicos. Retorna a quantidade inserida."""
    registros = list(registros)
    docs = [registro_to_document(r) for r in registros]
    file_paths = [r.fonte_url for r in registros]
    if docs:
        await rag.ainsert(docs, file_paths=file_paths)
    return len(docs)
