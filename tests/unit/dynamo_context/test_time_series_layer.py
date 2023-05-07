import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from boto3.dynamodb.conditions import Key

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from dynamo_context.python.time_series_layer import (
    build_key_expression,
    query_items,
)

@pytest.fixture
def current_timestamp():
    return int(datetime.now().timestamp())

# Test build_key_expression
def test_build_key_expression(current_timestamp):
    instrument = 'CORN'
    start_time = current_timestamp - 3600

    key_expression = build_key_expression(instrument, start_time)
    assert key_expression == Key('Instrument').eq(instrument) & Key('UnixDateTime').between(start_time, current_timestamp)

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