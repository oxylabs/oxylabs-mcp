# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

# Install the project into /app
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project --no-dev --no-editable

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-editable

# Final image
FROM python:3.12-slim-bookworm

WORKDIR /app

COPY --from=uv /root/.local /root/.local
COPY --from=uv --chown=app:app /app/.venv /app/.venv

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# When running the container, add your Oxylabs credentials as environment variables
ENTRYPOINT ["oxylabs_mcp"]