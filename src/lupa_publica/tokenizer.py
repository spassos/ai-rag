"""Tokenizer local, sem dependência de rede.

O tokenizer padrão do LightRAG usa ``tiktoken``, que baixa arquivos BPE da
internet na primeira execução. Isso quebra o teste offline no sandbox
(Constituição P9) e adiciona uma dependência externa em runtime. Usamos um
tokenizer por *codepoint* Unicode: ``encode``/``decode`` são lossless e a
contagem de tokens fica proporcional ao número de caracteres — suficiente para o
chunking do LightRAG.
"""

from __future__ import annotations

from lightrag.utils import Tokenizer


class CodepointTokenizer:
    """Tokenizer trivial: cada caractere vira seu codepoint Unicode."""

    def encode(self, content: str) -> list[int]:
        return [ord(c) for c in content]

    def decode(self, tokens: list[int]) -> str:
        return "".join(chr(t) for t in tokens)


def build_local_tokenizer() -> Tokenizer:
    """Retorna um ``Tokenizer`` do LightRAG baseado no tokenizer local."""
    return Tokenizer(model_name="lupa-local", tokenizer=CodepointTokenizer())
