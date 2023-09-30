#conftest.py

import pytest
import pandas as pd

# Fixture to mock a DataFrame similar to AEX.csv
@pytest.fixture
def mock_dataframe():
    data = {
        'DATETIME': ['2009-08-18 23:00:00', '2009-08-19 23:00:00'],
        'price': [89.57, 89.27]
    }
    return pd.DataFrame(data)

# Fixture to mock a DataFrame with empty values
@pytest.fixture
def mock_dataframe_with_empty_values():
    data = {
        'column1': [1, 2, None, 4],
        'column2': [None, 2, 3, 4]
    }
    return pd.DataFrame(data)
