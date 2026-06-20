"""Provedores de LLM/embeddings (abstração — ADR-004).

Hoje implementamos apenas o provedor ``fake`` (offline, determinístico) usado no
PoC e no smoke test. Vertex AI e Claude ficam como stubs documentados para a
Fase 4 do roadmap.
"""

from .base import BaseProvider
from .factory import get_provider

__all__ = ["BaseProvider", "get_provider"]
