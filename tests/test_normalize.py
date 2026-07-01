"""Testes da normalização e da renderização do documento canônico."""

from lupa_publica.ingest.normalize import (
    normalize_contrato,
    registro_to_document,
)


def test_normalize_formato_achatado():
    raw = {
        "documento_id": "CT-1",
        "orgao_codigo": "36000",
        "orgao_nome": "Ministério da Saúde",
        "fornecedor_cnpj": "11.111.111/0001-11",
        "fornecedor_nome": "ACME LTDA",
        "objeto": "seringas",
        "valor": 1000.5,
        "data": "2025-01-01",
    }
    r = normalize_contrato(raw)
    assert r.documento_id == "CT-1"
    assert r.orgao_nome == "Ministério da Saúde"
    assert r.valor == 1000.5
    # fonte_url é derivada quando ausente — obrigatória para citação (P1).
    assert r.fonte_url.endswith("/contratos/CT-1")


def test_normalize_formato_aninhado():
    raw = {
        "id": "CT-2",
        "orgao": {"codigo": "26000", "nome": "MEC"},
        "fornecedor": {"cnpj": "22.222.222/0001-22", "nome": "Beta SA"},
        "objeto": "merenda",
        "valor": 500,
    }
    r = normalize_contrato(raw)
    assert r.documento_id == "CT-2"
    assert r.orgao_nome == "MEC"
    assert r.fornecedor_nome == "Beta SA"


def test_documento_contem_fonte():
    raw = {"documento_id": "CT-3", "objeto": "x", "valor": 1, "fonte_url": "https://exemplo/CT-3"}
    doc = registro_to_document(normalize_contrato(raw))
    assert "Fonte: https://exemplo/CT-3" in doc
    assert "Documento: CT-3" in doc
