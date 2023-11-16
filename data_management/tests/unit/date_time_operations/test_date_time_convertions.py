import time

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.common_utils.errors.date_time_errors import (
    DateTimeConversionError,
    InvalidDatetimeColumnError,
)
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_column,
    convert_string_column_to_datetime,
    convert_datetime_to_unixtime,
)


@pytest.fixture
def time_based_dataframe():
    df = pd.DataFrame(
        {
            "time_str": ["2021-01-01", "2021-01-02"],
            "time_unix": [1609459200, 1609545600],
        }
    )
    return df


# Test for string-based time
def test_convert_string_to_datetime(time_based_dataframe):
    result = convert_string_column_to_datetime(time_based_dataframe, "time_str")
    expected_df = time_based_dataframe.copy()
    expected_df["time_str"] = pd.to_datetime(expected_df["time_str"])
    assert_frame_equal(result, expected_df)


# Test for Unix-based time
def test_convert_unix_to_datetime(time_based_dataframe):
    result = convert_string_column_to_datetime(time_based_dataframe, "time_unix", unit="s")
    expected_df = time_based_dataframe.copy()
    expected_df["time_unix"] = pd.to_datetime(expected_df["time_unix"], unit="s")
    assert_frame_equal(result, expected_df)


# Test for an Invalid column
def test_convert_invalid_column(time_based_dataframe):
    with pytest.raises(InvalidDatetimeColumnError):
        convert_string_column_to_datetime(time_based_dataframe, "invalid_column")


# Test for convert_column
def test_convert_column(time_based_dataframe):
    df = time_based_dataframe.copy()
    df["time_str"] = pd.to_datetime(df["time_str"])
    result = convert_column(time_based_dataframe, "time_str", None)
    assert_frame_equal(result, df)


# Test for convert_datetime_to_unixtime
def test_convert_datetime_to_unixtime(time_based_dataframe):
    df = time_based_dataframe.copy()
    df["time_str"] = pd.to_datetime(df["time_str"])
    df["time_unix_converted"] = df["time_str"].apply(
        lambda x: int(time.mktime(x.timetuple()))
    )
    result = convert_datetime_to_unixtime(df, "time_str")
    assert_frame_equal(result, df)


# Test for exception in convert_datetime_to_unixtime
def test_convert_datetime_to_unixtime_exception(time_based_dataframe):
    df = time_based_dataframe.copy()
    df["time_str"] = ["not_a_datetime", "2021-01-02"]
    with pytest.raises(DateTimeConversionError):
        convert_datetime_to_unixtime(df, "time_str")
