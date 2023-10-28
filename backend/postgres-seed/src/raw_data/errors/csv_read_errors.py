# custom_exceptions.py


class CsvFileNotFoundException(FileNotFoundError):
    """Raised when the CSV file is not found."""


class CsvEmptyDataError(Exception):
    """Raised when the CSV file contains no data."""


class CsvParserError(Exception):
    """Raised when there's a parsing error while reading the CSV file."""
