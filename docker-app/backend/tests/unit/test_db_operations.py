import pytest
from unittest.mock import Mock, patch
from src.database.db_operations import DatabaseManager

@pytest.fixture
def db_manager():
    return DatabaseManager()

def test_create(db_manager):
    table = "test_table"
    data = {"column1": "value1", "column2": "value2"}

    with patch.object(db_manager, "connection_cursor") as mock_connection_cursor:
        mock_cursor = Mock()
        mock_connection_cursor.return_value.__enter__.return_value = mock_cursor

        db_manager.create(table, data)

        assert mock_cursor.execute.called

def test_read(db_manager):
    table = "test_table"
    condition = "column1 = value1"

    with patch.object(db_manager, "connection_cursor") as mock_connection_cursor:
        mock_cursor = Mock()
        mock_connection_cursor.return_value.__enter__.return_value = mock_cursor

        db_manager.read(table, condition)

        assert mock_cursor.execute.called
        assert mock_cursor.fetchall.called

def test_update(db_manager):
    table = "test_table"
    data = {"column1": "value1"}
    condition = "column2 = value2"

    with patch.object(db_manager, "connection_cursor") as mock_connection_cursor:
        mock_cursor = Mock()
        mock_connection_cursor.return_value.__enter__.return_value = mock_cursor

        db_manager.update(table, data, condition)

        assert mock_cursor.execute.called

def test_delete(db_manager):
    table = "test_table"
    condition = "column1 = value1"

    with patch.object(db_manager, "connection_cursor") as mock_connection_cursor:
        mock_cursor = Mock()
        mock_connection_cursor.return_value.__enter__.return_value = mock_cursor

        db_manager.delete(table, condition)

        assert mock_cursor.execute.called
