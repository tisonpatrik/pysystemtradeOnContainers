import pandas as pd
from src.data_processing.data_frame_helper import convert_to_datetime_format, aggregate_to_day_based_prices


def test_aggregate_to_day_based_prices(sample_df, expected_df):
    # Call the function
    result_df = aggregate_to_day_based_prices(sample_df.copy(), 'price')
    
    # Check if the function returns the expected output
    pd.testing.assert_frame_equal(result_df, expected_df)

def test_convert_to_datetime_format(string_datetime_df):
    # Call the function to convert the DATETIME column to datetime format
    result_df = convert_to_datetime_format(string_datetime_df.copy(), 'DATETIME')
    
    # Check the dtype of the DATETIME column
    assert pd.api.types.is_datetime64_any_dtype(result_df['DATETIME'])