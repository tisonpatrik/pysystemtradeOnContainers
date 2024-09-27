
# Load environment variables from .env file
include ../.env
export

# Define MIGRATE_CMD with sslmode=disable for reuse
MIGRATE_CMD = docker run -v ./migrations/:/migrations --network pysystemtradeoncontainers_default migrate/migrate -path=/migrations/ -database "postgres://$(DB_USER):$(DB_PASSWORD)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)?sslmode=disable"

.PHONY:create_env
create_env:
	@env_generator/main

.PHONY:downoad_data
download_data:
	@downloader/main

.PHONY:process_data
process_data:
	@data_processing/main

.PHONY:resample_data
resample_data:
	python resampling/main.py


.PHONY:clean_data
clean_data:
	@data_cleaning/main

.PHONY:migrate_up
migrate_up:
	@$(MIGRATE_CMD) -verbose up

.PHONY:migrate_down
migrate_down:
	@$(MIGRATE_CMD) -verbose down

.PHONY:migrate_to_version
migrate_to_version:
	@$(MIGRATE_CMD) -verbose goto $(VERSION)

.PHONY:migrate_force
migrate_force:
	@$(MIGRATE_CMD) -verbose force $(VERSION)

.PHONY:clean
clean:
	@$(MIGRATE_CMD) -verbose drop -f

.PHONY:seed_config_data
seed_config_data:
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY instrument_config FROM '/data/csvconfig/instrumentconfig.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY instrument_metadata FROM '/data/csvconfig/moreinstrumentinfo.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY roll_config FROM '/data/csvconfig/rollconfig.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY spread_costs FROM '/data/csvconfig/spreadcosts.csv' DELIMITER ',' CSV HEADER"

.PHONY:seed_raw_data
seed_raw_data:
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY adjusted_prices FROM '/data/raw_data/adjusted_prices.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY fx_prices FROM '/data/raw_data/fx_prices.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY multiple_prices FROM '/data/raw_data/multiple_prices.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY roll_calendars FROM '/data/raw_data/roll_calendars.csv' DELIMITER ',' CSV HEADER"
