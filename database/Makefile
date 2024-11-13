
# Load environment variables from .env file
include ../.env
export

# Define MIGRATE_CMD with sslmode=disable for reuse
MIGRATE_CMD = docker run -v ./migrations/:/migrations --network pysystemtradeoncontainers_default migrate/migrate -path=/migrations/ -database "postgres://$(DB_USER):$(DB_PASSWORD)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)?sslmode=disable"

.PHONY: create_binaries
create_binaries:
	@for dir in downloader env_generator; do \
		echo "Building $$dir..."; \
		(cd $$dir && go build -o main -ldflags "-s -w"); \
	done

.PHONY:create_env
create_env:
	@env_generator/main

.PHONY:download_data
download_data:
	@downloader/main

.PHONY:migrate_up
migrate_up:
	@$(MIGRATE_CMD) -verbose up

.PHONY: migrate_down
migrate_down:
	@$(MIGRATE_CMD) -verbose down 999

.PHONY:migrate_to_version
migrate_to_version:
	@$(MIGRATE_CMD) -verbose goto $(VERSION)

.PHONY:migrate_force
migrate_force:
	@$(MIGRATE_CMD) -verbose force $(VERSION)

.PHONY:clean
clean:
	@$(MIGRATE_CMD) -verbose drop -f


.PHONY: seed_raw_data
seed_raw_data:
	@$(MAKE) seed_config_data
	@$(MAKE) seed_daily_adjusted_prices
	@$(MAKE) seed_daily_denominator_prices
	@$(MAKE) seed_multiple_prices
	@$(MAKE) seed_fx_prices
	@$(MAKE) seed_rules
	@$(MAKE) seed_fixed_scaling_factor

.PHONY:seed_config_data
seed_config_data:
	@for file in $$(docker exec -i $(DB_HOST) bash -c 'ls /data/instrumentconfig/*.csv'); do \
		echo "Processing file: $$file"; \
		docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY instrument_config FROM '$$file' DELIMITER ',' CSV HEADER"; \
	done

.PHONY: seed_daily_adjusted_prices
seed_daily_adjusted_prices:
	@for file in $$(docker exec -i $(DB_HOST) bash -c 'ls /data/daily_adjusted_prices/*.csv'); do \
		echo "Processing file: $$file"; \
		docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY daily_adjusted_prices FROM '$$file' DELIMITER ',' CSV HEADER"; \
	done

.PHONY: seed_daily_denominator_prices
seed_daily_denominator_prices:
	@for file in $$(docker exec -i $(DB_HOST) bash -c 'ls /data/daily_multiple_prices/*.csv'); do \
		echo "Processing file: $$file"; \
		docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY daily_denominator_prices FROM '$$file' DELIMITER ',' CSV HEADER"; \
	done

.PHONY: seed_multiple_prices
seed_multiple_prices:
	@for file in $$(docker exec -i $(DB_HOST) bash -c 'ls /data/multiple_prices/*.csv'); do \
		echo "Processing file: $$file"; \
		docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY multiple_prices FROM '$$file' DELIMITER ',' CSV HEADER"; \
	done

.PHONY: seed_fx_prices
seed_fx_prices:
	@for file in $$(docker exec -i $(DB_HOST) bash -c 'ls /data/fx_prices/*.csv'); do \
		echo "Processing file: $$file"; \
		docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY fx_prices FROM '$$file' DELIMITER ',' CSV HEADER"; \
	done

.PHONY: seed_rules
seed_rules:
	@for file in $$(docker exec -i $(DB_HOST) bash -c 'ls /data/rules/*.csv'); do \
		echo "Processing file: $$file"; \
		docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY rules FROM '$$file' DELIMITER ',' CSV HEADER"; \
	done
