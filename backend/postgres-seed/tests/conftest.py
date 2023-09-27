# fixture.py
import pytest_asyncio

@pytest_asyncio.fixture
def mock_connection(mocker):
    return mocker.Mock()

# Define AsyncContextManagerMock as a pytest fixture
@pytest_asyncio.fixture
def async_context_manager_mock():
    class AsyncContextManagerMock:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            pass

        def __call__(self):
            return self
    return AsyncContextManagerMock()