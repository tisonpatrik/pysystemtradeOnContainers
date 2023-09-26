from src.db.repositories.repository import PostgresRepository

def test_db_connection(db_connection):
    repo = PostgresRepository()
    assert repo._connect() is not None
    repo._disconnect(db_connection)