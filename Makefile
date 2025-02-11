src_dir := src/
test_dir := tests/
current_dir = $(shell pwd)

python ?= python3
virtualenv_dir ?= .venv

.PHONY: install_deps
install_deps: $(virtualenv_dir)
	uv sync

.PHONY: lint
lint: install_deps
	uv run mypy $(src_dir)
	uv run ruff check

.PHONY: format
format: $(virtualenv_dir)
	uv run ruff check --fix .

.PHONY: test
test: install_deps
	uv run pytest ./tests

.PHONY: run
run: install_deps
	npx @modelcontextprotocol/inspector@0.3.0 \
      uv \
      --directory $(current_dir) \
      run \
      oxylabs-mcp

$(virtualenv_dir):
	$(python) -m venv $@ --symlinks
