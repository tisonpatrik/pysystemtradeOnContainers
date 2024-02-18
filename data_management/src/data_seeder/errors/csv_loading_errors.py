class CsvLoadingError(Exception):
    """Exception raised for errors in the CSV loading process."""


class InvalidFileNameError(Exception):
    """
    Raised when an invalid file name is encountered in the processing pipeline.
    """
