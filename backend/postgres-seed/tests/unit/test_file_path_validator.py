import os
import tempfile
import pytest
from src.raw_data.errors.table_to_db_errors import InvalidFileNameError
from src.data_processor.data_processing.file_path_validator import FilePathValidator


@pytest.fixture
def validator():
    return FilePathValidator()


def test_get_full_path_valid_file(validator):
    with tempfile.NamedTemporaryFile() as temp_file:
        directory, file_name = os.path.split(temp_file.name)
        result = validator.get_full_path(directory, file_name)
        assert result == temp_file.name


def test_get_full_path_invalid_file(validator):
    with pytest.raises(InvalidFileNameError):
        validator.get_full_path("/not/a/real/directory", "fake_file.txt")
