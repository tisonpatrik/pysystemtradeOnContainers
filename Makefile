.PHONY: init dev run stop down tests migration_up migration_down

create_db_env:
	@database/env_generator/main

process_data:
	@database/data_processing/main

cheers:
	@echo "Na zdraví! 🍺"

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

# Calling migration targets from the Makefile in the database directory
migration_up:
	@$(MAKE) -C database migration_up

migration_down:
	@$(MAKE) -C database migration_down

migration_force:
	@$(MAKE) -C database migration_force

migration_step_up:
	@$(MAKE) -C database migration_step_up

migration_step_down:
	@$(MAKE) -C database migration_step_down
