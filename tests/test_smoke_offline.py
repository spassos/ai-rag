"""Smoke test offline do pipeline completo (Constituição P9).

Roda normalização → indexação (LightRAG file-based) → consulta, tudo com o
provedor fake, sem rede nem credenciais. Valida que a resposta:
1. recupera o documento correto (seringas/saúde);
2. vem **fundamentada** com a fonte oficial (RF4).
"""

import asyncio
import json
from pathlib import Path

from lupa_publica.app import run_pipeline
from lupa_publica.config import Settings

FIXTURE = Path(__file__).parent / "fixtures" / "contratos_sample.json"


def test_pipeline_offline_responde_com_fonte(tmp_path):
    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
    settings = Settings(provider="fake", working_dir=str(tmp_path / "rag"))

    ans = asyncio.run(
        run_pipeline(settings, raw, "contratos de seringas para a saúde")
    )

    assert ans.grounded, "a resposta deve citar ao menos uma fonte (RF4)"
    assert any("CT-2025-0001" in c for c in ans.citations), ans.citations
    assert "CT-2025-0001" in ans.context


def test_pipeline_pergunta_sem_correspondencia(tmp_path):
    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
    settings = Settings(provider="fake", working_dir=str(tmp_path / "rag"))

    ans = asyncio.run(
        run_pipeline(settings, raw, "xpto zzz qwerty inexistente nenhum termo")
    )
    # Sem correspondência, não inventa: declara ausência de dados (EARS-4.2).
    assert "não há dados suficientes" in ans.answer.lower() or not ans.grounded
