import pytest
import pandas as pd
from src.data_processing.data_frame_helper import convert_to_datetime_format, aggregate_to_day_based_prices

# Fixture for sample DataFrame
@pytest.fixture(scope='module')
def sample_df():
    sample_data = {
        'unix_date_time': ['2022-01-01 23:00:00', '2022-01-01 23:10:00', '2022-01-02 23:00:00'],
        'price': [100, 110, 120]
    }
    return pd.DataFrame(sample_data)

@pytest.fixture(scope='module')
def expected_df():
    expected_data = {
        'unix_date_time': pd.to_datetime(['2022-01-01', '2022-01-02']),  # Ensure datetime dtype
        'price': [105.0, 120.0]  # Changed to float to match the dtype in result_df
    }
    return pd.DataFrame(expected_data)

def test_aggregate_to_day_based_prices(sample_df, expected_df):
    # Convert to datetime format before aggregation
    sample_df = convert_to_datetime_format(sample_df.copy(), 'unix_date_time')
    
    # Call the function
    result_df = aggregate_to_day_based_prices(sample_df.copy())
    
    # Check if the function returns the expected output
    pd.testing.assert_frame_equal(result_df, expected_df)

def test_convert_to_datetime_format(sample_df):
    # Call the function to convert the DATETIME column to datetime format
    result_df = convert_to_datetime_format(sample_df.copy(), 'unix_date_time')
    
    # Check the dtype of the DATETIME column
    assert pd.api.types.is_datetime64_any_dtype(result_df['unix_date_time'])
