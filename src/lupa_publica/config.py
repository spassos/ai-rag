"""Configuração da aplicação, lida de variáveis de ambiente (.env)."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=False)


@dataclass(frozen=True)
class Settings:
    """Parâmetros de execução da Lupa Pública.

    Tudo tem default seguro para rodar **offline** no sandbox.
    """

    provider: str = "fake"
    working_dir: str = ".lupa/rag"
    top_k: int = 5
    cosine_threshold: float = 0.15

    # Ingestão online (não usada no smoke offline).
    transparencia_api_key: str = ""
    transparencia_base_url: str = "https://api.portaldatransparencia.gov.br/api-de-dados"

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            provider=os.getenv("LUPA_PROVIDER", "fake"),
            working_dir=os.getenv("LUPA_WORKING_DIR", ".lupa/rag"),
            top_k=int(os.getenv("LUPA_TOP_K", "5")),
            cosine_threshold=float(os.getenv("LUPA_COSINE_THRESHOLD", "0.15")),
            transparencia_api_key=os.getenv("TRANSPARENCIA_API_KEY", ""),
            transparencia_base_url=os.getenv(
                "TRANSPARENCIA_BASE_URL",
                "https://api.portaldatransparencia.gov.br/api-de-dados",
            ),
        )
