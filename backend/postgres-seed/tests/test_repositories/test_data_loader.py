# import pytest
# from unittest.mock import patch, MagicMock
# from src.db.repositories.data_loader import DataLoader
# from src.db.errors import DatabaseConnectionError, TableOrColumnNotFoundError

# @pytest.mark.asyncio
# async def test_fetch_data_async():
#     mock_pool = MagicMock()
#     mock_pool.acquire().__aenter__().prepare().fetch.return_value = [
#         {"column1": "value1", "column2": "value2"}
#     ]

#     with patch("asyncpg.create_pool", return_value=mock_pool) as mock_create_pool:
#         loader = DataLoader("fake_database_url")
#         rows = await loader.fetch_data_async("SELECT * FROM table WHERE id=$id", {"id": 1})

#     mock_create_pool.assert_called_once_with(dsn="fake_database_url")
#     assert rows == [{"column1": "value1", "column2": "value2"}]

# @pytest.mark.asyncio
# async def test_fetch_data_async_connection_error():
#     with patch("asyncpg.create_pool", side_effect=Exception("Connection error")):
#         loader = DataLoader("fake_database_url")
        
#         with pytest.raises(DatabaseConnectionError):
#             await loader.fetch_data_async("SELECT * FROM table WHERE id=$id", {"id": 1})

# @pytest.mark.asyncio
# async def test_fetch_data_async_table_not_found():
#     mock_pool = MagicMock()
#     mock_pool.acquire().__aenter__().prepare.side_effect = Exception("Table not found")

#     with patch("asyncpg.create_pool", return_value=mock_pool):
#         loader = DataLoader("fake_database_url")
        
#         with pytest.raises(TableOrColumnNotFoundError):
#             await loader.fetch_data_async("SELECT * FROM invalid_table WHERE id=$id", {"id": 1})
