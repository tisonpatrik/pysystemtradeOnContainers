# backend/postgres-seed/db/Dockerfile
# pull official base image
FROM postgres:15.3

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d

WORKDIR /home/app/db

COPY config_schemas.sql /home/app/db/config_schemas.sql
COPY raw_data_schemas.sql /home/app/db/raw_data_schemas.sql
COPY risk_schemas.sql /home/app/db/risk_schemas.sql
