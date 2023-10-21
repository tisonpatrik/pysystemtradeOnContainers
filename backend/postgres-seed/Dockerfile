# backend/postgres-seed/Dockerfile
# Using the specified Python version
FROM python:3.10-slim-bookworm AS base

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl git build-essential \
    && apt-get autoremove -y
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -


FROM base AS install
# Setting the working directory in the container
WORKDIR /home/app

# allow controlling the poetry installation of dependencies via external args
ARG INSTALL_ARGS="--no-root"
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
COPY postgres-seed/pyproject.toml postgres-seed/poetry.lock* ./ 

# install without virtualenv, since we are inside a container
RUN poetry config virtualenvs.create false \
    && poetry install $INSTALL_ARGS

# cleanup
#RUN curl -sSL https://install.python-poetry.org | python3 - --uninstall
RUN apt-get purge -y curl git build-essential \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*


FROM install as app-image
ENV PYTHONPATH=/home/app/ PYTHONHASHSEED=0


# Copying the source code to the working directory
COPY postgres-seed/src ./src
COPY postgres-seed/tests ./tests
COPY postgres-seed/alembic ./alembic
COPY postgres-seed/db ./db
COPY postgres-seed/mappings ./mappings

# Copying the shared directory into the container
COPY ../shared /home/app/shared

# Specifying the default command to run the FastAPI app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
