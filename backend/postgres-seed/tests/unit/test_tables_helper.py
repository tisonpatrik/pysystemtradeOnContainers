import pytest
import pandas as pd

from src.data_processor.errors.table_helper_errors import ColumnRenameError, MissingColumnsError
from src.data_processor.data_processing.tables_helper import TablesHelper

@pytest.fixture
def service_instance():
    return TablesHelper()

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({'old_name1': [1, 2], 'old_name2': [3, 4]})

def test_rename_columns_with_valid_mapping(service_instance, sample_dataframe):
    new_column_names = {'old_name1': 'new_name1', 'old_name2': 'new_name2'}
    renamed_df = service_instance.rename_columns(sample_dataframe, new_column_names)
    assert list(renamed_df.columns) == ['new_name1', 'new_name2']

def test_rename_columns_with_missing_columns(service_instance, sample_dataframe):
    new_column_names = {'old_name1': 'new_name1', 'non_existent_column': 'new_name2'}
    with pytest.raises(MissingColumnsError):
        service_instance.rename_columns(sample_dataframe, new_column_names)

def test_rename_columns_with_exception_during_rename(service_instance, sample_dataframe):
    new_column_names = {'old_name1': 'new_name1', 'old_name2': None}  # None should cause an exception
    with pytest.raises(ColumnRenameError):
        service_instance.rename_columns(sample_dataframe, new_column_names)
