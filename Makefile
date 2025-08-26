src_dir := src/
test_dir := tests/
current_dir = $(shell pwd)

python ?= python3
virtualenv_dir ?= .venv

.PHONY: install_deps
install_deps: $(virtualenv_dir)
	uv sync --group dev

.PHONY: lint
lint: install_deps
	uv run black --check .
	uv run mypy $(src_dir)
	uv run ruff check

.PHONY: format
format: $(virtualenv_dir)
	uv run black .
	uv run ruff check --fix .

.PHONY: test
test: install_deps
	uv run pytest --cov=src --cov-report xml --cov-report term --cov-fail-under=90 tests/unit tests/integration

.PHONY: test-e2e
test-e2e:
	uv sync --group dev --group e2e-tests
	uv run pytest --cov=src --cov-report xml --cov-report term tests/e2e

.PHONY: run
run: install_deps
	npx @modelcontextprotocol/inspector \
      uv \
      --directory $(current_dir) \
      run \
      oxylabs-mcp

$(virtualenv_dir):
	$(python) -m venv $@ --symlinks

.PHONY: checkdeps
checkdeps: $(virtualenv_dir)
	uv lock --check

.PHONY: sectest
sectest: $(virtualenv_dir)
	uv sync
	uv run bandit -c pyproject.toml -r $(src_dir)
