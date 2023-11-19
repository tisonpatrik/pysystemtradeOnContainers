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
	@docker exec -it data_management poetry run pytest

migrate-create:
	@alembic revision --autogenerate -m "${commit}"

migrate-apply:
	@alembic upgrade head