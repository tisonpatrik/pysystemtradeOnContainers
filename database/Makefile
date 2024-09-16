.PHONY: build run stop migration_up migration_down force_version clean seed_config_data seed_raw_data

# Load environment variables from .env file
include ../.env
export

# Define MIGRATE_CMD with sslmode=disable for reuse
MIGRATE_CMD = docker run -v ./migrations/:/migrations --network grayfox_default migrate/migrate -path=/migrations/ -database "postgres://$(DB_USER):$(DB_PASSWORD)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)?sslmode=disable"

# Run migrations up
migrate_up:
	@$(MIGRATE_CMD) -verbose up

# Run migrations down
migrate_down:
	@$(MIGRATE_CMD) -verbose down

# Migrate to a specific version
migrate_to_version:
	@$(MIGRATE_CMD) -verbose goto $(VERSION)

# Force the database version (fix dirty database state)
force_version:
	@$(MIGRATE_CMD) -verbose force $(VERSION)

# Clean migration state
clean:
	@$(MIGRATE_CMD) -verbose drop -f

# Seed the database with CSV config data
seed_config_data:
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY instrument_config FROM '/data/config_data/instrumentconfig.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY instrument_metadata FROM '/data/config_data/moreinstrumentinfo.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY roll_config FROM '/data/config_data/rollconfig.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY spread_costs FROM '/data/config_data/spreadcosts.csv' DELIMITER ',' CSV HEADER"

# Seed the database with CSV raw data
seed_raw_data:
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY adjusted_prices FROM '/data/raw_data/adjusted_prices.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY fx_prices FROM '/data/raw_data/fx_prices.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY multiple_prices FROM '/data/raw_data/multiple_prices.csv' DELIMITER ',' CSV HEADER"
	@docker exec -i $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME) -c "\COPY roll_calendars FROM '/data/raw_data/roll_calendars.csv' DELIMITER ',' CSV HEADER"
