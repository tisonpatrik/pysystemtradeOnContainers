import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_datetime_to_unixtime,
)
from src.common_utils.errors.date_time_errors import DateTimeConversionError


@pytest.fixture
def time_based_dataframe():
    mock_data = {
        "DATETIME": pd.to_datetime(
            [
                "2022-09-21 15:00:00",
                "2022-09-21 19:00:00",
                "2022-09-22 14:30:00",
                "2022-09-22 23:00:00",
                "2022-09-23 15:00:00",
                "2022-09-23 23:00:00",
            ]
        ),
        "PRICE": [95.14, 95.39, 93.18, 93.86, 92.97, 92.69],
    }
    return pd.DataFrame(mock_data)


def test_convert_datetime_to_unixtime_success(time_based_dataframe):
    converted_df = convert_datetime_to_unixtime(time_based_dataframe, "DATETIME")
    expected_data = {
        "DATETIME": [
            1663772400,
            1663786800,
            1663857000,
            1663887600,
            1663945200,
            1663974000,
        ],
        "PRICE": [95.14, 95.39, 93.18, 93.86, 92.97, 92.69],
    }
    expected_df = pd.DataFrame(expected_data)
    assert_frame_equal(converted_df, expected_df)


def test_convert_datetime_to_unixtime_failure(time_based_dataframe):
    with pytest.raises(DateTimeConversionError):
        convert_datetime_to_unixtime(time_based_dataframe, "NON_EXISTENT_COLUMN")
