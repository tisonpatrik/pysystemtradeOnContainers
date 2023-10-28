import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from src.common_utils.utils.column_operations.add_and_populate_column import (
    add_column_and_populate_it_by_value,
)
from src.common_utils.errors.rename_colums_errors import SymbolAdditionError


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({"old_name1": [1.111, 2.222], "old_name2": [3.333, 4.444]})


# Test for successful addition of a new column
def test_add_column_and_populate_it_by_value_success(sample_dataframe):
    expected_df = sample_dataframe.copy()
    expected_df["new_column"] = "value"
    result_df = add_column_and_populate_it_by_value(
        sample_dataframe.copy(), "new_column", "value"
    )
    assert_frame_equal(result_df, expected_df)
