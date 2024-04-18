FROM python:3.12-alpine AS base

RUN apk update \
    && apk upgrade \
    && apk add --no-cache curl git build-base \
    && rm -rf /var/cache/apk/*

# Setting the working directory in the container
WORKDIR /home/app

COPY common/ ./common
COPY raw_data ./raw_data
COPY risk ./risk

COPY seeder/ ./seeder
COPY .env ./

RUN pip install --no-cache-dir -r seeder/requirements.txt

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
