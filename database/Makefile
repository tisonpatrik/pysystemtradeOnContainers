.PHONY: build run stop migration_up migration_down force_version clean seed_config_data seed_raw_data

# Load environment variables from .env file
include .env
export

# CLI commands for migrations (use localhost or 127.0.0.1)
MIGRATE_CMD = migrate -path ./migrations/ -database "postgres://$(DB_USER):$(DB_PASSWORD)@127.0.0.1:$(DB_PORT)/$(DB_NAME)?sslmode=$(DB_SSLMODE)"

# Build the database Docker image with a proper name
build:
	@docker build --build-arg DB_USER=$(DB_USER) --build-arg DB_PASSWORD=$(DB_PASSWORD) --build-arg DB_NAME=$(DB_NAME) -t timescale_image -f ./Dockerfile .

# Run the database container
run: build
	@docker run --name timescale_container -e POSTGRES_PASSWORD=$(DB_PASSWORD) -e DB_USER=$(DB_USER) -e DB_PASSWORD=$(DB_PASSWORD) -e DB_NAME=$(DB_NAME) -p 5432:5432 -v $(PWD)/data:/data -d timescale_image

# Stop the database container
stop:
	@docker stop $(DB_HOST)
	@docker rm $(DB_HOST)

# Run migrations up
migration_up:
	@$(MIGRATE_CMD) -verbose up

# Run migrations down
migration_down:
	@$(MIGRATE_CMD) -verbose down

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
