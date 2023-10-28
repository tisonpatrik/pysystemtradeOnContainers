import os
import tempfile
import pytest
from src.raw_data.errors.table_to_db_errors import InvalidFileNameError
from src.raw_data.utils.path_validator import get_full_path


def test_get_full_path_valid_file():
    with tempfile.NamedTemporaryFile() as temp_file:
        directory, file_name = os.path.split(temp_file.name)
        result = get_full_path(directory, file_name)
        assert result == temp_file.name


def test_get_full_path_invalid_file():
    with pytest.raises(InvalidFileNameError):
        get_full_path("/not/a/real/directory", "fake_file.txt")
