FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=2

RUN apt update && \
    apt upgrade -y && \
    apt clean && \
    rm -rf /var/cache/apt/*

FROM base AS uv
ENV UV_PYTHON_PREFERENCE=only-system \
    UV_PYTHON_DOWNLOADS=never \
    UV_NO_CACHE=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local/

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
ENV PATH="/root/.local/bin:${PATH}"

FROM uv AS dev
WORKDIR /app
COPY rules/pyproject.toml rules/uv.lock rules/README.md ./

RUN uv sync --frozen

FROM uv AS prod
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
COPY rules/pyproject.toml rules/uv.lock rules/README.md ./

COPY common/ /common/
RUN uv sync --no-dev

COPY rules/src/rules/ /app/rules
COPY .env ./

RUN adduser --disabled-password --gecos '' myuser && \
    chown -R myuser:myuser /app

USER myuser

CMD ["python", "-m", "rules.main"]