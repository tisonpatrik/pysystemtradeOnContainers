# Načtení proměnných z .env souboru
include .env
export

# CLI příkazy pro migrace
MIGRATE_CMD = migrate -path ./migrations/ -database "postgres://$(DB_USER):$(DB_PASSWORD)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)?sslmode=$(DB_SSLMODE)"
migration_up:
	@$(MIGRATE_CMD) -verbose up

migration_down:
	@$(MIGRATE_CMD) -verbose down
