.PHONY: install lint test smoke check

install:
	pip install -e ".[dev]"

lint:
	ruff check src tests

test:
	pytest

smoke:
	./scripts/local_smoke.sh

# Mesmo conjunto que o CI roda (gate P9 antes de qualquer deploy).
check: lint test smoke
