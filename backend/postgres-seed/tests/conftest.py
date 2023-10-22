# conftest.py
import pytest
from src.csv_io.schemas.csv_output import CsvOutput


# Fixture to mock a DataFrame similar to AEX.csv
@pytest.fixture
def mock_csv_mappings():
    return [
        CsvOutput(
            full_path="/path/to/csv1",
            table="table1",
            data=[
                {"col1": "value11", "col2": "value12"},
                {"col1": "value21", "col2": "value22"},
            ],
        ),
        CsvOutput(
            full_path="/path/to/csv2",
            table="table2",
            data=[
                {"col1": "value31", "col2": "value32"},
                {"col1": "value41", "col2": "value42"},
            ],
        ),
    ]
