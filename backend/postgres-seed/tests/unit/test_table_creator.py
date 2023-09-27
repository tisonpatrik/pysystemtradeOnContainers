import pytest
from src.db.table_creator import TableCreator

# Test __init__ method
def test_init(mock_connection):
    table_creator = TableCreator(mock_connection)
    assert table_creator.connection == mock_connection

# Test create_table with successful execution
@pytest.mark.asyncio
async def test_create_table_success(mock_connection, mocker):
    async def mock_execute(sql):
        pass
    
    mock_connection.execute = mock_execute
    sql_command = "CREATE TABLE test (id SERIAL PRIMARY KEY);"

    mock_logger = mocker.patch('src.db.table_creator.logger')
    table_creator = TableCreator(mock_connection)
    await table_creator.create_table(sql_command)

    mock_logger.info.assert_has_calls([
        mocker.call("Successfully executed the following SQL command: %s", sql_command),
        mocker.call("Database connection closed.")
    ])

# Test create_table with failed execution
@pytest.mark.asyncio
async def test_create_table_fail(mock_connection, mocker):
    async def mock_execute(sql):
        raise Exception("Some error")

    mock_connection.execute = mock_execute
    sql_command = "CREATE TABLE test (id SERIAL WRONG KEY);"

    mock_logger = mocker.patch('src.db.table_creator.logger')
    table_creator = TableCreator(mock_connection)
    await table_creator.create_table(sql_command)

    # Get the last call's arguments
    args, kwargs = mock_logger.error.call_args

    # Check the format string
    assert args[0] == "Failed to execute the SQL command due to: %s"
    
    # Check the exception's string representation
    assert str(args[1]) == "Some error"

# Test create_table finally block
@pytest.mark.asyncio
async def test_create_table_finally(mock_connection, mocker):
    async def mock_execute(sql):
        pass

    mock_connection.execute = mock_execute
    sql_command = "CREATE TABLE test (id SERIAL PRIMARY KEY);"

    mock_logger = mocker.patch('src.db.table_creator.logger')
    table_creator = TableCreator(mock_connection)
    await table_creator.create_table(sql_command)

    mock_logger.info.assert_called_with("Database connection closed.")
