"""Cliente da API do Portal da Transparência (RF1).

Dois modos:

- **offline** (``from_fixture``): lê registros de um JSON local — usado no smoke
  test do sandbox, sem rede nem chave de API (Constituição P9).
- **online** (``fetch_contratos``): chama a API real. Requer chave de API e
  **não** é exercitado nos testes. Mantido simples e com paginação básica.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

from ..config import Settings


def load_fixture(path: str | Path) -> list[dict]:
    """Carrega registros brutos de um arquivo JSON (lista de objetos)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Fixture deve conter uma lista de registros JSON.")
    return data


class TransparenciaClient:
    """Cliente HTTP mínimo para a API de Dados do Portal da Transparência."""

    def __init__(self, settings: Settings) -> None:
        self.base_url = settings.transparencia_base_url
        self.api_key = settings.transparencia_api_key

    def fetch_contratos(self, *, codigo_orgao: str, pagina: int = 1) -> list[dict]:
        """Busca contratos de um órgão (online).

        Levanta erro se a chave de API não estiver configurada — o caminho
        offline (``load_fixture``) deve ser usado no sandbox.
        """
        if not self.api_key:
            raise RuntimeError(
                "TRANSPARENCIA_API_KEY ausente. Para rodar offline use as fixtures "
                "(load_fixture) — ver Constituição P9."
            )
        params = urllib.parse.urlencode({"codigoOrgao": codigo_orgao, "pagina": pagina})
        url = f"{self.base_url.rstrip('/')}/contratos?{params}"
        req = urllib.request.Request(url, headers={"chave-api-dados": self.api_key})
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))
