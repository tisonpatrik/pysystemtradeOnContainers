import pandas as pd
import pytest

# Fixture for sample DataFrame
@pytest.fixture(scope='module')
def sample_df():
    sample_data = {
        'DATETIME': ['2022-01-01 23:00:00', '2022-01-01 23:10:00', '2022-01-02 23:00:00'],
        'price': [100, 110, 120]
    }
    return pd.DataFrame(sample_data)

@pytest.fixture(scope='module')
def expected_df():
    expected_data = {
        'DATETIME': pd.to_datetime(['2022-01-01', '2022-01-02']),  # Ensure datetime dtype
        'price': [105.0, 120.0]  # Changed to float to match the dtype in result_df
    }
    return pd.DataFrame(expected_data)


# Fixture for DataFrame with string-formatted datetime
@pytest.fixture(scope='module')
def string_datetime_df():
    sample_data = {
        'DATETIME': ['2022-01-01 23:00:00', '2022-01-01 23:10:00', '2022-01-02 23:00:00'],
        'price': [100, 110, 120]
    }
    return pd.DataFrame(sample_data)