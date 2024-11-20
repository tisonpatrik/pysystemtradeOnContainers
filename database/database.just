set dotenv-load

default:
    @just --list --unsorted

# Define MIGRATE_CMD with sslmode=disable for reuse
MIGRATE_CMD := docker run -v ./migrations/:/migrations --network pysystemtradeoncontainers_default migrate/migrate -path=/migrations/ -database "postgres://{{env.DB_USER}}:{{env.DB_PASSWORD}}@{{env.DB_HOST}}:{{env.DB_PORT}}/{{env.DB_NAME}}?sslmode=disable"

create_binaries:
    @for dir in downloader env_generator; do \
        echo "Building $$dir..."; \
        (cd $$dir && go build -o main -ldflags "-s -w"); \
    done

create_env:
    @env_generator/main

download_data:
    @downloader/main

migrate_up:
    @{{MIGRATE_CMD}} -verbose up

migrate_down:
    @{{MIGRATE_CMD}} -verbose down 999

migrate_to_version:
    @{{MIGRATE_CMD}} -verbose goto {{VERSION}}

migrate_force:
    @{{MIGRATE_CMD}} -verbose force {{VERSION}}

drop_database:
    @{{MIGRATE_CMD}} -verbose drop -f

seed_raw_data:
    @just seed_config_data
    @just seed_daily_adjusted_prices
    @just seed_daily_denominator_prices
    @just seed_multiple_prices
    @just seed_fx_prices
    @just seed_rules
    @just seed_fixed_scaling_factor

seed_config_data:
    @for file in $$(docker exec -i {{env.DB_HOST}} bash -c 'ls /data/instrumentconfig/*.csv'); do \
        echo "Processing file: $$file"; \
        docker exec -i {{env.DB_HOST}} psql -U {{env.DB_USER}} -d {{env.DB_NAME}} -c "\COPY instrument_config FROM '$$file' DELIMITER ',' CSV HEADER"; \
    done

seed_daily_adjusted_prices:
    @for file in $$(docker exec -i {{env.DB_HOST}} bash -c 'ls /data/daily_adjusted_prices/*.csv'); do \
        echo "Processing file: $$file"; \
        docker exec -i {{env.DB_HOST}} psql -U {{env.DB_USER}} -d {{env.DB_NAME}} -c "\COPY daily_adjusted_prices FROM '$$file' DELIMITER ',' CSV HEADER"; \
    done

seed_daily_denominator_prices:
    @for file in $$(docker exec -i {{env.DB_HOST}} bash -c 'ls /data/daily_multiple_prices/*.csv'); do \
        echo "Processing file: $$file"; \
        docker exec -i {{env.DB_HOST}} psql -U {{env.DB_USER}} -d {{env.DB_NAME}} -c "\COPY daily_denominator_prices FROM '$$file' DELIMITER ',' CSV HEADER"; \
    done

seed_multiple_prices:
    @for file in $$(docker exec -i {{env.DB_HOST}} bash -c 'ls /data/multiple_prices/*.csv'); do \
        echo "Processing file: $$file"; \
        docker exec -i {{env.DB_HOST}} psql -U {{env.DB_USER}} -d {{env.DB_NAME}} -c "\COPY multiple_prices FROM '$$file' DELIMITER ',' CSV HEADER"; \
    done

seed_fx_prices:
    @for file in $$(docker exec -i {{env.DB_HOST}} bash -c 'ls /data/fx_prices/*.csv'); do \
        echo "Processing file: $$file"; \
        docker exec -i {{env.DB_HOST}} psql -U {{env.DB_USER}} -d {{env.DB_NAME}} -c "\COPY fx_prices FROM '$$file' DELIMITER ',' CSV HEADER"; \
    done

seed_rules:
    @for file in $$(docker exec -i {{env.DB_HOST}} bash -c 'ls /data/rules/*.csv'); do \
        echo "Processing file: $$file";
