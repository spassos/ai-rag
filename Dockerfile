# Imagem do serviço de consulta / job de ingestão da Lupa Pública.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml requirements.txt README.md ./
COPY src ./src
COPY tests ./tests
COPY scripts ./scripts

RUN pip install --upgrade pip && pip install -e .

# Default: roda o smoke offline. No Cloud Run, o entrypoint do serviço HTTP será
# definido quando a API web for implementada (Fase 5).
CMD ["python", "-m", "lupa_publica.cli", "smoke"]
