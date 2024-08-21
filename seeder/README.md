# Seeder Service
## Database Table Creation

Before seeding data, you must create the necessary tables in the database. If you're using `pipenv`, you can achieve this by running:

```bash
pipenv run alembic stamp head
```
Make sure that the sqlalchemy.url in your `alembic.ini` file is correctly set to match your .env file configuration.
By default, it should look like this:
```bash
sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost/postgres
```
## Seeding Data

This service provides (for now) just two endpoints for seeding data. You need to call these endpoints in the specified order
from port 8100 to correctly initialize the data:

- seed_config_data_route
- seed_raw_data_route

## Modifying Database Schemas

If you need to modify the Alembic database schemas, you'll find them in `seeder/db_models/db_models.py`.
After making changes, apply the following commands to update the schema:

```bash
pipenv run alembic upgrade head
pipenv run alembic revision --autogenerate -m "some comment about your changes"
pipenv run alembic upgrade head
```

## Final Note

I'm really hate the complexity of this setup.... requiring the original project,
pysystemtrade_preprocessing, the seeder service, alembic and gods knows what else...
So, if anyone has ideas on how to simplify this process (perhaps with a terminal application?), any help would be greatly appreciated!
