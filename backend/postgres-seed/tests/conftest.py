# fixture.py
import pytest_asyncio
from unittest.mock import Mock

@pytest_asyncio.fixture
def mock_connection():
    return Mock()