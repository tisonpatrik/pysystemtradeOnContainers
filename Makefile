.PHONY: cheers
cheers:
	@echo "Na zdraví! 🍺🍺🍺🍺🍺"

.PHONY: init
init:
	@echo "Initializing environment..."
	@$(MAKE) -C database create_env
	@echo "Processing data..."
	@$(MAKE) -C database download_data
	@$(MAKE) -C database process_data
	@$(MAKE) -C database resample_data
	@echo "Running the app..."
	@$(MAKE) run  # Call the run method from this Makefile
	@sleep 10  # Add a 10-second timeout
	@echo "Running remaining migrations"
	@$(MAKE) -C database migrate_up
	@echo "Seeding config data..."
	@$(MAKE) -C database seed_config_data
	@echo "Seeding raw data...This may take a few minutes.."
	@$(MAKE) -C database seed_raw_data
	@$(MAKE) -C database clean_data
	@echo "Initialization complete!"

.PHONY: clean
clean:
	@$(MAKE) -C database clean

.PHONY: migrate
migrate:
	@$(MAKE) -C database migrate_up

.PHONY: dev
dev:
	@docker compose -f docker-compose.yml up --build

.PHONY: run
run:
	@docker compose -f docker-compose.yml up --build -d

.PHONY: stop
stop:
	@docker compose -f docker-compose.yml down

.PHONY: down
down:
	@docker compose -f ./docker-compose.yml down --remove-orphans

.PHONY: tests
tests: run
	@echo "IMPLEMENT IT"
