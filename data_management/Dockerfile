FROM python:3.12-alpine AS base

RUN apk update \
    && apk upgrade \
    && apk add --no-cache curl git build-base \
    && rm -rf /var/cache/apk/*

# Setting the working directory in the container
WORKDIR /home/app

COPY common/ ./common

COPY data_management/src/ ./src
COPY data_management/tests/ ./tests

COPY data_management/.env ./
COPY data_management/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
