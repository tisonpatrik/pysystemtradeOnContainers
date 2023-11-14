import pandas as pd
import pytest

from src.common_utils.errors.rename_colums_errors import MissingColumnsError
from src.common_utils.utils.column_operations.rename_columns import rename_columns


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {"Column1": [1, 2, 3], "Column2": [4, 5, 6], "Unnamed: 1": [7, 8, 9]}
    )


def test_rename_columns_success(sample_dataframe):
    new_column_names = {"Column1": "NewColumn1", "Column2": "NewColumn2"}
    renamed_df = rename_columns(sample_dataframe, new_column_names)
    assert list(renamed_df.columns) == ["NewColumn1", "NewColumn2", "Unnamed: 1"]


def test_rename_columns_missing_columns(sample_dataframe):
    new_column_names = {"NonExistentColumn": "NewName"}
    with pytest.raises(MissingColumnsError):
        rename_columns(sample_dataframe, new_column_names)
