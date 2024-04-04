FROM python:3.12.2-slim as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_HOME=/opt/poetry 

RUN python3 -m venv ${POETRY_HOME} && ${POETRY_HOME}/bin/pip install poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR $POETRY_HOME/bin/poetry install --without dev --no-root --no-interaction

FROM builder as test-builder

RUN --mount=type=cache,target=$POETRY_CACHE_DIR $POETRY_HOME/bin/poetry install --with dev --no-root --no-interaction

FROM python:3.12.2-slim as tests

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$POETRY_HOME/bin:$PATH" \
    PYTHONPATH=/app/ \
    PYTHONUNBUFFERED=1

COPY --from=test-builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY src src

ENTRYPOINT ["pytest"]


FROM python:3.12.2-slim as production

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$POETRY_HOME/bin:$PATH" \
    PYTHONPATH=/app/ \
    PYTHONUNBUFFERED=1

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app
COPY src/app app
ENTRYPOINT ["uvicorn", "app.core.application:app", "--host", "0.0.0.0", "--port", "8080"]
