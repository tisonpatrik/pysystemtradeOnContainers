import pytest
from src.db.table_creator import TableCreator

@pytest.mark.asyncio
async def test_create_table_integration(db_connection):
    table_creator = TableCreator(db_connection)
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    );
    """
    await table_creator.create_table(create_table_sql)
    
    # Verify that the table was actually created
    async with db_connection.transaction():
        row = await db_connection.fetchrow("SELECT to_regclass('public.test_table');")
        assert row and row['to_regclass'] == 'test_table'

    # Cleanup: Drop the test table to maintain a clean state
    await db_connection.execute("DROP TABLE test_table;")