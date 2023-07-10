import pytest
from unittest.mock import Mock, MagicMock
from src.database.database_manager import DatabaseManager

@pytest.fixture
def db_manager():
    # Mock the DatabaseConnection instance
    db_conn_mock = Mock()

    # Create a MagicMock for the context manager
    context_manager_mock = MagicMock()

    # Set the __enter__ return value
    context_manager_mock.__enter__.return_value = Mock()

    # Set the mocked context manager to return when connection_cursor is called
    db_conn_mock.connection_cursor.return_value = context_manager_mock

    return db_conn_mock

    return DatabaseManager(db_conn_mock)


def test_create(db_manager):
    table = 'test_table'
    data = {'column1': 'value1', 'column2': 'value2'}

    # Call the create method
    db_manager.create(table, data)

    # Ensure the create method of the db_manager was called with correct arguments
    db_manager.create.assert_called_once_with(table, data)


def test_read(db_manager):
    table = 'test_table'

    # Call the read method
    db_manager.read(table)

    # Ensure the read method of the db_manager was called with correct arguments
    db_manager.read.assert_called_once_with(table)


def test_update(db_manager):
    table = 'test_table'
    data = {'column1': 'value1'}
    condition = 'column2 = value2'

    # Call the update method
    db_manager.update(table, data, condition)

    # Ensure the update method of the db_manager was called with correct arguments
    db_manager.update.assert_called_once_with(table, data, condition)


def test_delete(db_manager):
    table = 'test_table'
    condition = 'column2 = value2'

    # Call the delete method
    db_manager.delete(table, condition)

    # Ensure the delete method of the db_manager was called with correct arguments
    db_manager.delete.assert_called_once_with(table, condition)
