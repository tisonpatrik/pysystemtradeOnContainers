import 'common/protos.just'
# import 'database/database.just'

cheers:
    @echo "Na zdraví! 🍺🍺🍺🍺🍺"

init:
    @echo "Create binaries"
    @just create_binaries
    @echo "Initializing environment..."
    @just create_env
    @echo "Processing data..."
    @just download_data
    @echo "Running the app..."
    @just run
    @sleep 5  # Add a 5-second timeout
    @echo "Running remaining migrations"
    @just migrate_up
    @echo "Seeding raw data...This may take a few minutes.."
    @just seed_raw_data
    @echo "Initialization complete!"

drop_database:
    @just drop_database

migrate:
    @just migrate_up

protos:
    @just generate_protos

dev:
    @docker compose -f docker-compose.yml up --build

run:
    @docker compose -f docker-compose.yml up --build -d

stop:
    @docker compose -f docker-compose.yml down

down:
    @docker compose -f docker-compose.yml down --remove-orphans

tests:
    @echo "IMPLEMENT IT"

rows:
    @sh -c 'find . -type d -name "src" | while IFS= read -r dir; do find "$dir" -type f -name "*.py" -exec cat {} +; done | wc -l'
