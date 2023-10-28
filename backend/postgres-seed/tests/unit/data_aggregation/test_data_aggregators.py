import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.common_utils.errors.aggregation_errors import DataAggregationError
from src.common_utils.utils.data_aggregation.data_aggregators import (
    aggregate_to_day_based_prices,
)


@pytest.fixture
def time_based_dataframe():
    df = pd.DataFrame(
        {
            "date_time": [
                "2021-01-01 12:00:00",
                "2021-01-01 14:00:00",
                "2021-01-02 12:00:00",
            ],
            "price": [100.0, 110.0, 105.0],
        }
    )
    df["date_time"] = pd.to_datetime(df["date_time"])
    return df


# Test with a DataFrame that has multiple entries for a single day.
def test_aggregate_to_day_based_prices_single_day_multiple_entries(
    time_based_dataframe,
):
    # Adding extra data to the fixture for a single day
    extra_data = pd.DataFrame(
        {
            "date_time": ["2021-01-01 16:00:00", "2021-01-01 18:00:00"],
            "price": [120.0, 130.0],
        }
    )
    extra_data["date_time"] = pd.to_datetime(extra_data["date_time"])
    test_df = pd.concat([time_based_dataframe, extra_data], ignore_index=True)

    expected_result = pd.DataFrame(
        {
            "date_time": ["2021-01-01", "2021-01-02"],
            "price": [(100 + 110 + 120 + 130) / 4, 105],
        }
    )
    expected_result["date_time"] = pd.to_datetime(expected_result["date_time"])

    result = aggregate_to_day_based_prices(test_df, "date_time")

    assert_frame_equal(result, expected_result)


# Test with already aggerated.
def test_aggregate_to_day_based_prices_already_daily():
    # Define the DataFrame that already consists of daily data
    test_df = pd.DataFrame(
        {"date_time": ["2021-01-01", "2021-01-02"], "price": [100, 105]}
    )
    test_df["date_time"] = pd.to_datetime(test_df["date_time"])

    expected_result = test_df.copy().astype(
        {"price": "float64"}
    )  # Update dtype to float64

    result = aggregate_to_day_based_prices(test_df, "date_time")

    assert_frame_equal(result, expected_result)


# Test with invalid date_time_column input.
def test_aggregate_to_day_based_prices_invalid_datetime_column(time_based_dataframe):
    # Intentionally providing an incorrect datetime column name
    invalid_column_name = "invalid_column"

    with pytest.raises(DataAggregationError):
        aggregate_to_day_based_prices(time_based_dataframe, invalid_column_name)


# Test with empty DataFrame
def test_aggregate_to_day_based_prices_empty_dataframe():
    # Create an empty DataFrame
    empty_dataframe = pd.DataFrame()

    with pytest.raises(DataAggregationError):
        aggregate_to_day_based_prices(empty_dataframe, "DATETIME")
