import pandas as pd
import pytest

from src.common_utils.errors.rounding_error import ColumnRoundingError
from src.raw_data.utils.round_column_numbers import (
    round_values_in_column,
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {"column1": [1.111, 2.222, 3.333], "column2": [4.444, 5.555, 6.666]}
    )


# Test: Normal case
def test_round_values_in_column(sample_dataframe):
    rounded_df = round_values_in_column(sample_dataframe, "column1")
    assert all(rounded_df["column1"] == [1.1, 2.2, 3.3])


# Test: Column is string
def test_round_values_in_column_string_column(sample_dataframe):
    # Add a column with string data to sample_dataframe
    sample_dataframe["string_column"] = ["a", "b", "c"]
    with pytest.raises(ColumnRoundingError):
        round_values_in_column(sample_dataframe, "string_column")
