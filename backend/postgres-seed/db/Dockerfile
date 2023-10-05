# backend/postgres-seed/db/Dockerfile
# pull official base image
FROM postgres:15.3

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d

WORKDIR /home/gx/code

COPY instrument_config.sql /home/gx/code/instrument_config.sql
COPY instrument_metadata.sql /home/gx/code/instrument_metadata.sql
COPY roll_config.sql /home/gx/code/roll_config.sql
COPY spread_cost.sql /home/gx/code/spread_cost.sql
