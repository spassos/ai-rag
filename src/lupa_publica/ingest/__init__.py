"""Ingestão e normalização de dados do Portal da Transparência (RF1)."""

from .normalize import Registro, normalize_contrato, registro_to_document

__all__ = ["Registro", "normalize_contrato", "registro_to_document"]
