"""Normalização para o esquema canônico (ver docs/spec/04-data-sources.md).

Cada registro vira um documento textual com campos rotulados, incluindo a linha
``Fonte:`` — obrigatória para a citação de fonte (Constituição P1).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Registro:
    """Registro canônico de um gasto público (subset para o PoC: contratos)."""

    documento_id: str
    tipo: str
    orgao_codigo: str
    orgao_nome: str
    fornecedor_cnpj: str
    fornecedor_nome: str
    objeto: str
    valor: float
    data: str
    fonte_url: str

    def as_dict(self) -> dict:
        return asdict(self)


def _fmt_valor(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def build_fonte_url(base_url: str, documento_id: str) -> str:
    """Monta um link estável para o registro oficial."""
    return f"{base_url.rstrip('/')}/contratos/{documento_id}"


def normalize_contrato(
    raw: dict, base_url: str = "https://portaldatransparencia.gov.br"
) -> Registro:
    """Converte um registro bruto de contrato no :class:`Registro` canônico.

    Aceita tanto o formato achatado das fixtures quanto chaves aninhadas comuns
    na API. Campos ausentes viram string vazia / 0.0 (entidade incompleta,
    sinalizável depois).
    """
    documento_id = str(
        raw.get("documento_id")
        or raw.get("id")
        or raw.get("numero")
        or raw.get("numeroContrato")
        or "DESCONHECIDO"
    )
    orgao = raw.get("orgao") if isinstance(raw.get("orgao"), dict) else {}
    fornecedor = raw.get("fornecedor") if isinstance(raw.get("fornecedor"), dict) else {}

    return Registro(
        documento_id=documento_id,
        tipo=str(raw.get("tipo", "contrato")),
        orgao_codigo=str(raw.get("orgao_codigo") or orgao.get("codigo", "")),
        orgao_nome=str(raw.get("orgao_nome") or orgao.get("nome", "")),
        fornecedor_cnpj=str(raw.get("fornecedor_cnpj") or fornecedor.get("cnpj", "")),
        fornecedor_nome=str(raw.get("fornecedor_nome") or fornecedor.get("nome", "")),
        objeto=str(raw.get("objeto", "")),
        valor=float(raw.get("valor", 0) or 0),
        data=str(raw.get("data") or raw.get("dataAssinatura", "")),
        fonte_url=str(raw.get("fonte_url") or build_fonte_url(base_url, documento_id)),
    )


def registro_to_document(r: Registro) -> str:
    """Renderiza o registro como texto rotulado para indexação no LightRAG."""
    return (
        f"Documento: {r.documento_id}\n"
        f"Tipo: {r.tipo}\n"
        f"Órgão: {r.orgao_nome} (código {r.orgao_codigo})\n"
        f"Fornecedor: {r.fornecedor_nome} (CNPJ {r.fornecedor_cnpj})\n"
        f"Objeto: {r.objeto}\n"
        f"Valor: {_fmt_valor(r.valor)}\n"
        f"Data: {r.data}\n"
        f"Fonte: {r.fonte_url}"
    )
