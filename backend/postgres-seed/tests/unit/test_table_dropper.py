import pytest
from src.db.table_dropper import TableDropper

# Test __init__ method
def test_init_dropper(mock_connection):
    table_dropper = TableDropper(mock_connection)
    assert table_dropper.connection == mock_connection

# Test drop_all_tables with successful execution
@pytest.mark.asyncio
async def test_drop_all_tables_success(mock_connection, mocker, async_context_manager_mock):
    async def mock_execute(sql):
        pass

    mock_connection.execute = mock_execute
    mock_connection.transaction = async_context_manager_mock  # Make it callable

    mock_logger = mocker.patch('src.db.table_dropper.logger')
    table_dropper = TableDropper(mock_connection)
    await table_dropper.drop_all_tables_async()

    mock_logger.info.assert_called_with("Successfully dropped all tables and indexes from the database")

# Test drop_all_tables with failed execution
@pytest.mark.asyncio
async def test_drop_all_tables_fail(mock_connection, mocker, async_context_manager_mock):
    async def mock_execute(sql):
        raise Exception("Some error")

    mock_connection.execute = mock_execute
    mock_connection.transaction = async_context_manager_mock  # Make it callable

    mock_logger = mocker.patch('src.db.table_dropper.logger')

    with pytest.raises(Exception):  # Expecting an exception to be raised
        table_dropper = TableDropper(mock_connection)
        await table_dropper.drop_all_tables_async()

    call_args = mock_logger.error.call_args
    if call_args is not None:
        args, kwargs = call_args
        assert args[0] == "Failed to drop tables and indexes due to: %s"
        assert str(args[1]) == "Some error"
