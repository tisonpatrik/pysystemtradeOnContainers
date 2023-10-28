import pytest
import pandas as pd

from src.common_utils.utils.column_operations.rename_columns import rename_columns
from src.common_utils.utils.column_operations.add_and_populate_column import (
    add_column_and_populate_it_by_value,
)
from src.common_utils.utils.column_operations.round_column_numbers import (
    round_values_in_column,
)
from src.common_utils.errors.rename_colums_errors import (
    ColumnRenameError,
    MissingColumnsError,
    ColumnRoundingError,
    SymbolAdditionError,
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({"old_name1": [1.111, 2.222], "old_name2": [3.333, 4.444]})


def test_rename_columns_with_valid_mapping(sample_dataframe):
    new_column_names = {"old_name1": "new_name1", "old_name2": "new_name2"}
    renamed_df = rename_columns(sample_dataframe, new_column_names)
    assert list(renamed_df.columns) == ["new_name1", "new_name2"]


def test_rename_columns_with_missing_columns(sample_dataframe):
    new_column_names = {"old_name1": "new_name1", "non_existent_column": "new_name2"}
    with pytest.raises(MissingColumnsError):
        rename_columns(sample_dataframe, new_column_names)


def test_rename_columns_with_exception_during_rename(sample_dataframe):
    new_column_names = {
        "old_name1": "new_name1",
        "old_name2": None,
    }  # None should cause an exception
    with pytest.raises(ColumnRenameError):
        rename_columns(sample_dataframe, new_column_names)


def test_rename_columns_with_none_values(sample_dataframe):
    new_column_names = {
        "old_name1": None,
        "old_name2": "new_name2",
    }  # None should cause an exception
    with pytest.raises(ColumnRenameError):
        rename_columns(sample_dataframe, new_column_names)


# Test for round_values_in_column
def test_round_values_in_column_success(sample_dataframe):
    rounded_df = round_values_in_column(sample_dataframe, "old_name1")
    assert all(rounded_df["old_name1"] == [1.1, 2.2])


def test_round_values_in_column_failure(sample_dataframe):
    with pytest.raises(ColumnRoundingError):
        round_values_in_column(sample_dataframe, "non_existent_column")


# Test for add_column_and_populate_it_by_value
def test_add_column_and_populate_it_by_value_success(sample_dataframe):
    new_df = add_column_and_populate_it_by_value(
        sample_dataframe, "new_column", "value"
    )
    assert "new_column" in new_df.columns
    assert all(new_df["new_column"] == "value")


# def test_add_column_and_populate_it_by_value_failure(sample_dataframe):
#     with pytest.raises(SymbolAdditionError):
#         bad_dataframe = (
#             "Not a DataFrame"  # This is not a DataFrame, should raise an error
#         )
#         add_column_and_populate_it_by_value(bad_dataframe, "new_column", "value")
