"""Provedor ``fake``: offline e determinístico, para testes e smoke no sandbox.

- ``embed``: embedding *bag-of-words* por hashing — textos que compartilham
  palavras ficam próximos no espaço vetorial, dando retrieval com significado,
  sem rede nem credenciais.
- ``llm``: stub que retorna vazio (não extrai entidades durante a indexação).
- ``generate``: compõe uma resposta **estritamente fundamentada** no contexto
  recuperado, sem inventar nada (Constituição P1).
"""

from __future__ import annotations

import hashlib
import re

import numpy as np

from .base import BaseProvider

_WORD = re.compile(r"\w+", re.UNICODE)
_DOC_BLOCK = re.compile(r"Documento:\s*(?P<id>\S+)")
_FIELD = lambda name: re.compile(rf"{name}:\s*(?P<v>.+)")  # noqa: E731


class FakeProvider(BaseProvider):
    name = "fake"

    def __init__(self, embedding_dim: int = 64) -> None:
        self.embedding_dim = embedding_dim

    def _embed_one(self, text: str) -> np.ndarray:
        vec = np.zeros(self.embedding_dim, dtype=np.float32)
        for tok in _WORD.findall(text.lower()):
            idx = int(hashlib.md5(tok.encode()).hexdigest(), 16) % self.embedding_dim
            vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        return vec / norm if norm else vec

    async def embed(self, texts: list[str]) -> np.ndarray:
        return np.array([self._embed_one(t) for t in texts], dtype=np.float32)

    async def llm(
        self,
        prompt: str,
        system_prompt: str | None = None,
        history_messages: list | None = None,
        **kwargs: object,
    ) -> str:
        # Sem LLM real: não extrai entidades. Retornamos o delimitador de conclusão
        # do LightRAG para que a extração termine limpa (zero entidades, sem
        # warnings). O retrieval naive (vetorial) basta para o PoC offline.
        return "<|COMPLETE|>"

    async def generate(self, question: str, context: str) -> str:
        registros = self._parse_registros(context)
        if not registros:
            return (
                "Não há dados suficientes no acervo para responder a esta pergunta. "
                "(provedor offline 'fake')"
            )
        linhas = [
            f"Pergunta: {question}",
            f"Encontrei {len(registros)} registro(s) relevante(s) nos dados públicos:",
        ]
        for r in registros:
            partes = [f"- Documento {r['id']}"]
            if r.get("Órgão"):
                partes.append(f"órgão: {r['Órgão']}")
            if r.get("Objeto"):
                partes.append(f"objeto: {r['Objeto']}")
            if r.get("Valor"):
                partes.append(f"valor: {r['Valor']}")
            linhas.append("; ".join(partes) + ".")
        linhas.append(
            "\nResposta gerada por provedor offline (sem LLM real): apenas lista os "
            "registros recuperados, sem interpretação. As fontes oficiais estão citadas abaixo."
        )
        return "\n".join(linhas)

    @staticmethod
    def _parse_registros(context: str) -> list[dict]:
        """Extrai os blocos de documento do contexto recuperado."""
        registros: list[dict] = []
        # O contexto pode conter \n escapados (JSON) ou reais; normalizamos.
        texto = context.replace("\\n", "\n")
        blocos = re.split(r"(?=Documento:\s*\S+)", texto)
        for bloco in blocos:
            m = _DOC_BLOCK.search(bloco)
            if not m:
                continue
            reg: dict = {"id": m.group("id").strip()}
            for campo in ("Órgão", "Fornecedor", "Objeto", "Valor", "Fonte", "Tipo", "Data"):
                fm = _FIELD(campo).search(bloco)
                if fm:
                    reg[campo] = fm.group("v").strip().strip('"').rstrip("\\")
            registros.append(reg)
        return registros
