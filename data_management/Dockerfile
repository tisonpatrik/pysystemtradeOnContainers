# data_management/Dockerfile
# Using the specified Python version
FROM python:3.12-slim-bookworm AS base

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl git build-essential \
    && apt-get autoremove -y

# Setting the working directory in the container
WORKDIR /home/app

# Copying the poetry dependency files to the working directory
COPY data_management/pyproject.toml data_management/poetry.lock* ./

# Copying the source code and other directories to the working directory
COPY data_management/src/ ./src
COPY data_management/tests/ ./tests
COPY data_management/mappings/ ./mappings

# Copying the shared directory - ensure this path is correct relative to the Dockerfile
COPY ../shared ./shared

# Installing poetry and the project dependencies
RUN pip install poetry

# Disabling virtualenv creation by poetry and installing dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main

# cleanup
RUN apt-get purge -y curl git build-essential \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*

ENV PYTHONPATH=/home/app/ PYTHONHASHSEED=0

# Specifying the default command to run the FastAPI app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
