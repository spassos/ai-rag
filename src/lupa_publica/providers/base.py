"""Interface comum dos provedores de LLM/embeddings."""

from __future__ import annotations

import abc

import numpy as np


class BaseProvider(abc.ABC):
    """Contrato que todo provedor (fake, Vertex, Claude) deve cumprir.

    A mesma interface é consumida pelo LightRAG (``embed`` e ``llm``) e pela
    camada de consulta (``generate``).
    """

    #: Nome curto do provedor (ex.: "fake").
    name: str = "base"
    #: Dimensão dos vetores de embedding produzidos por ``embed``.
    embedding_dim: int = 64

    @abc.abstractmethod
    async def embed(self, texts: list[str]) -> np.ndarray:
        """Gera embeddings (shape ``[len(texts), embedding_dim]``)."""

    @abc.abstractmethod
    async def llm(
        self,
        prompt: str,
        system_prompt: str | None = None,
        history_messages: list | None = None,
        **kwargs: object,
    ) -> str:
        """Função de LLM usada pelo LightRAG durante a indexação."""

    @abc.abstractmethod
    async def generate(self, question: str, context: str) -> str:
        """Gera a resposta final ao usuário, **fundamentada** no contexto.

        Deve respeitar a Constituição P1: não inventar dados; se o contexto for
        insuficiente, declarar que não há dados suficientes.
        """
