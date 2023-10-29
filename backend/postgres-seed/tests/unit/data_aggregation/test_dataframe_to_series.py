import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from src.common_utils.errors.dataframe_to_series_errors import (
    ColumnNotFoundError,
    GroupByError,
    DataFrameConversionError,
)
from src.common_utils.utils.data_aggregation.dataframe_to_series import (
    get_grouped_df,
    convert_group_to_series,
    convert_dataframe_to_dict_of_series,
)


@pytest.fixture
def time_based_dataframe():
    data = {
        "symbol": ["AAPL", "AAPL", "MSFT", "MSFT", "GOOGL"],
        "timestamp": pd.date_range(start="1/1/2021", periods=5, freq="D"),
        "value": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)
    return df


# Test successful grouping
def test_get_grouped_df_success(time_based_dataframe):
    grouped_dict = get_grouped_df(time_based_dataframe, "symbol")
    assert "AAPL" in grouped_dict
    assert "MSFT" in grouped_dict
    assert "GOOGL" in grouped_dict


# Test for generic Exception
def test_get_grouped_df_general_error(time_based_dataframe):
    with pytest.raises(GroupByError):
        # Deliberately inducing an error by passing a DataFrame object instead of string
        get_grouped_df(time_based_dataframe, time_based_dataframe)


@pytest.fixture
def grouped_dataframe_dict():
    data_1 = {
        "symbol": ["AAPL", "AAPL"],
        "timestamp": pd.date_range(start="1/1/2021", periods=2, freq="D"),
        "value": [1, 2],
    }
    data_2 = {
        "symbol": ["MSFT", "MSFT"],
        "timestamp": pd.date_range(start="1/3/2021", periods=2, freq="D"),
        "value": [3, 4],
    }
    df_1 = pd.DataFrame(data_1)
    df_2 = pd.DataFrame(data_2)
    return {"AAPL": df_1, "MSFT": df_2}


# Test successful conversion
def test_convert_group_to_series_success(grouped_dataframe_dict):
    result = convert_group_to_series(grouped_dataframe_dict, "symbol", "timestamp")
    assert "AAPL" in result  # Only expecting 'AAPL'
    assert isinstance(result["AAPL"], pd.Series)


# Test for KeyError scenario for symbol_column
def test_convert_group_to_series_symbol_key_error(grouped_dataframe_dict):
    with pytest.raises(KeyError):
        convert_group_to_series(grouped_dataframe_dict, "unknown_symbol", "timestamp")


# Test for KeyError scenario for index_column
def test_convert_group_to_series_index_key_error(grouped_dataframe_dict):
    with pytest.raises(KeyError):
        convert_group_to_series(grouped_dataframe_dict, "symbol", "unknown_timestamp")
