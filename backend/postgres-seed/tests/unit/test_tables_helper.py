import pytest
import pandas as pd

from src.data_processor.errors.table_helper_errors import ColumnRenameError, MissingColumnsError, ColumnRoundingError, SymbolAdditionError
from src.data_processor.data_processing.tables_helper import TablesHelper

@pytest.fixture
def service_instance():
    return TablesHelper()

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({'old_name1': [1.111, 2.222], 'old_name2': [3.333, 4.444]})

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

def test_rename_columns_with_none_values(service_instance, sample_dataframe):
    new_column_names = {'old_name1': None, 'old_name2': 'new_name2'}  # None should cause an exception
    with pytest.raises(ColumnRenameError):
        service_instance.rename_columns(sample_dataframe, new_column_names)

# Test for round_values_in_column
def test_round_values_in_column_success(service_instance, sample_dataframe):
    rounded_df = service_instance.round_values_in_column(sample_dataframe, 'old_name1')
    assert all(rounded_df['old_name1'] == [1.1, 2.2])

def test_round_values_in_column_failure(service_instance, sample_dataframe):
    with pytest.raises(ColumnRoundingError):
        service_instance.round_values_in_column(sample_dataframe, 'non_existent_column')

# Test for add_column_and_populate_it_by_value
def test_add_column_and_populate_it_by_value_success(service_instance, sample_dataframe):
    new_df = service_instance.add_column_and_populate_it_by_value(sample_dataframe, 'new_column', 'value')
    assert 'new_column' in new_df.columns
    assert all(new_df['new_column'] == 'value')

def test_add_column_and_populate_it_by_value_failure(service_instance, sample_dataframe):
    with pytest.raises(SymbolAdditionError):
        bad_dataframe = "Not a DataFrame"  # This is not a DataFrame, should raise an error
        service_instance.add_column_and_populate_it_by_value(bad_dataframe, 'new_column', 'value')