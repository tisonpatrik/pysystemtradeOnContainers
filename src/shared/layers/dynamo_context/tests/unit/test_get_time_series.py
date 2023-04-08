import pytest
import aioboto3
from unittest.mock import AsyncMock
from boto3.dynamodb.conditions import Key

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from dynamo_context.python.get_time_series import (
    build_key_expression,
    query_items,
    scan_items,
    get_time_series_from_dynamodb,
)

# Test build_key_expression
def test_build_key_expression():
    instrument = "TEST_INSTRUMENT"
    start_time = 1620000000

    key_expr = build_key_expression(instrument, start_time)

    assert isinstance(key_expr, Key)
    assert key_expr.to_dict()["condition"].startswith("(attribute_exists(Instrument) AND Instrument =")

# Test query_items
@pytest.mark.asyncio
async def test_query_items():
    key_expr = Key("Instrument").eq("TEST_INSTRUMENT")
    mock_table = AsyncMock()
    mock_table.query.side_effect = [
        {"Items": ["item1"], "LastEvaluatedKey": "key1"},
        {"Items": ["item2"], "LastEvaluatedKey": "key2"},
        {"Items": ["item3"]}
    ]

    items = await query_items(mock_table, key_expr)

    assert items == ["item1", "item2", "item3"]

# Test scan_items
@pytest.mark.asyncio
async def test_scan_items():
    key_expr = Key("Instrument").eq("TEST_INSTRUMENT")
    mock_table = AsyncMock()
    mock_table.scan.side_effect = [
        {"Items": ["item1"], "LastEvaluatedKey": "key1"},
        {"Items": ["item2"], "LastEvaluatedKey": "key2"},
        {"Items": ["item3"]}
    ]

    items = await scan_items(mock_table, key_expr)

    assert items == ["item1", "item2", "item3"]

# Test get_time_series_from_dynamodb
@pytest.mark.asyncio
async def test_get_time_series_from_dynamodb(monkeypatch):
    table_name = "TestTable"
    instrument = "TEST_INSTRUMENT"
    start_time = 1620000000

    async def mock_query_items(*args, **kwargs):
        return ["item1", "item2", "item3"]

    async def mock_scan_items(*args, **kwargs):
        return ["item1", "item2", "item3"]

    monkeypatch.setattr(aioboto3, "resource", AsyncMock(return_value=AsyncMock()))
    monkeypatch.setattr("forecasting.src.common.get_time_series.query_items", mock_query_items)
    monkeypatch.setattr("forecasting.src.common.get_time_series.scan_items", mock_scan_items)

    items = await get_time_series_from_dynamodb(table_name, instrument, start_time)

    assert items == ["item1", "item2", "item3"]
