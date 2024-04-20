from typing import Any, Sequence, Union


class Statement:
    def __init__(self, table_name: str, query: str, parameters: Union[Any, Sequence[Any]]):
        # Directly store parameters if it's a sequence and not a string
        # This avoids wrapping a list (your symbols) in a tuple unnecessarily
        if isinstance(parameters, Sequence) and not isinstance(parameters, str):
            self._parameters = parameters
        else:
            self._parameters = (parameters,)  # Wrap non-sequence items in a tuple
        self._query = query
        self._table_name = table_name

    @property
    def table_name(self) -> str:
        """Returns the table name."""
        return self._table_name

    @property
    def query(self) -> str:
        """Returns the SQL query string."""
        return self._query

    @property
    def parameters(self) -> Union[list[Any], tuple[Any, ...]]:
        """Ensures parameters are returned in an expected sequence type."""
        # Correctly handle the conversion or direct return based on the _parameters type
        if isinstance(self._parameters, tuple):
            return self._parameters  # Directly return if it's already a tuple
        else:
            return (self._parameters,)  # Wrap non-sequence and non-list items in a tuple
