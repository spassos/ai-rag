#!/usr/bin/env bash
# Teste local offline (Constituição P9): roda o pipeline completo com o provedor
# fake, sem rede nem credenciais. É o mesmo gate executado no CI antes de
# qualquer deploy na GCP.
set -euo pipefail

cd "$(dirname "$0")/.."

export LUPA_PROVIDER=fake
# Evita que qualquer biblioteca tente baixar tokenizers da internet.
export TIKTOKEN_CACHE_DIR="${TIKTOKEN_CACHE_DIR:-/tmp/lupa-tiktoken}"

echo "==> Smoke test offline da Lupa Pública"
python -m lupa_publica.cli smoke "$@"
echo "==> Smoke test concluído com sucesso"
