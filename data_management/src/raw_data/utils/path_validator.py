"""
Provides utilities for validating file paths and raising appropriate exceptions.
"""

import os

from src.raw_data.errors.path_validation_error import InvalidFileNameError


def get_full_path(directory: str, file_name: str) -> str:
    """
    Validates the full file path constructed from the provided directory and file_name.
    """
    full_path = os.path.join(directory, file_name)
    if not os.path.exists(full_path):
        raise InvalidFileNameError(f"File path {full_path} does not exist.")
    return full_path
