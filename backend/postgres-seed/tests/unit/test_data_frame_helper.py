import pytest
from src.data_processing.data_frame_helper import (
    rename_columns,
    fill_empty_values
    )
from src.data_processing.errors import(
    ColumnRenameError,
    EmptyValueFillError
)

# Mock logger for testing
class MockLogger:
    def error(self, *args):
        pass

logger = MockLogger()

def test_rename_columns_success(mock_dataframe):
    new_column_names = {"DATETIME": "unix_date_time", "price": "price"}
    renamed_df = rename_columns(mock_dataframe, new_column_names)
    assert list(renamed_df.columns) == ['unix_date_time', 'price']

def test_rename_columns_fail(mock_dataframe):
    new_column_names = {"wrong_column": "unix_date_time", "price": "price"}
    with pytest.raises(ColumnRenameError):
        rename_columns(mock_dataframe, new_column_names)

def test_fill_empty_values_success(mock_dataframe_with_empty_values):
    fill_value = 0
    filled_df = fill_empty_values(mock_dataframe_with_empty_values, fill_value)
    assert filled_df.isna().sum().sum() == 0  # Check that there are no NaN values in the DataFrame

def test_fill_empty_values_fail(mock_dataframe_with_empty_values):
    fill_value = {'wrong_column': 0}
    with pytest.raises(EmptyValueFillError):
        fill_empty_values(mock_dataframe_with_empty_values, fill_value)
