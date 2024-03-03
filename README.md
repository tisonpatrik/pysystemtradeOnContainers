# grayfox
pipenv run alembic upgrade head

pipenv run alembic revision --autogenerate -m "Update models"

pipenv run alembic upgrade head
