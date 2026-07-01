"""Seleção do provedor conforme a configuração (ADR-004)."""

from __future__ import annotations

from ..config import Settings
from .base import BaseProvider
from .fake import FakeProvider


def get_provider(settings: Settings) -> BaseProvider:
    """Instancia o provedor indicado em ``settings.provider``.

    Apenas ``fake`` está implementado no PoC. ``vertex`` e ``claude`` ficam para
    a Fase 4 do roadmap — quando implementados, devem cumprir ``BaseProvider``.
    """
    nome = settings.provider.lower()
    if nome == "fake":
        return FakeProvider()
    if nome in {"vertex", "claude"}:
        raise NotImplementedError(
            f"Provedor '{nome}' ainda não implementado (ver roadmap Fase 4). "
            "Use LUPA_PROVIDER=fake para rodar offline."
        )
    raise ValueError(f"Provedor desconhecido: {settings.provider!r}")
