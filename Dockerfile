FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/opt/uv-cache/

RUN apt-get update && apt-get install -y --no-install-recommends git

WORKDIR /app

RUN --mount=type=cache,target=UV_CACHE_DIR \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --no-editable

ADD . /app

RUN --mount=type=cache,target=UV_CACHE_DIR \
    uv sync --frozen --no-dev --no-editable

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["oxylabs-mcp"]
