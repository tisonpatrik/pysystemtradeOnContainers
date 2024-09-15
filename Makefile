.PHONY: cheers dev run stop down tests

cheers:
	@echo "Na zdraví! 🍺🍺🍺🍺🍺"

init:
	@echo "Initializing environment..."
	@database/env_generator/main
	@echo "Processing data..."
	@database/data_processing/main
	@echo "Migrating database to version $(VERSION)..."
	@$(MAKE) -C database migrate_to_version "VERSION=3"
	@echo "Seeding config data..."
	@$(MAKE) -C database seed_config_data
	@echo "Seeding raw data... This may take a few minutes."
	@$(MAKE) -C database seed_raw_data
	@echo "Running remaining migrations..."
	@$(MAKE) -C database migrate_up
	@echo "Initialization complete!"

clean:
	@$(MAKE) -C database clean


dev:
	@docker compose -f docker-compose.yml up --build

run:
	@docker compose -f docker-compose.yml up --build -d

stop:
	@docker compose -f docker-compose.yml down

down:
	@docker compose -f ./docker-compose.yml down --remove-orphans

tests: run
	@echo "IMPLEMENT IT"
