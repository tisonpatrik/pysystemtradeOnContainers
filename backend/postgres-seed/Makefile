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
	@docker exec -it postgres-seed poetry run pytest

migrate-create:
	@poetry run alembic revision --autogenerate -m "${commit}"

migrate-apply:
	@poetry run alembic upgrade head

build:
	@poetry shell
	@poetry run black .
	@poetry run isort . --profile black
	@poetry run pylint **/*.py