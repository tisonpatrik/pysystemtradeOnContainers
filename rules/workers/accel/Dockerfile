FROM python:3.12-alpine AS base

# Install necessary packages
RUN apk update \
    && apk upgrade \
    && apk add --no-cache curl git build-base \
    && rm -rf /var/cache/apk/*

# Setting the working directory in the container
WORKDIR /home/app

# Copy the application files
COPY rules/workers/accel/ ./accel
COPY common/ ./common
COPY rules/workers/shared/ ./shared

# Install Python dependencies
RUN pip install --no-cache-dir -r accel/requirements.txt

# Set the entry point to run Celery
CMD ["celery", "-A", "accel.accel", "worker", "--loglevel=info", "-Q", "accel"]
