from typing import Any, Optional, Union


class FetchStatement:
    """Statement class for encapsulating data fetching parameters. This class utilizes the table name provided to format or validate queries."""

    def __init__(self, query: str, parameters: Optional[Union[str, tuple[Any, ...]]] = None):
        self._query = query
        # Ensure parameters are stored as a tuple, handling single, multiple or no parameter cases.
        if parameters is not None:
            if isinstance(parameters, str):
                self._parameters = (parameters,)  # Make single non-tuple parameter into a tuple
            else:
                self._parameters = parameters
        else:
            self._parameters = tuple()

    @property
    def query(self) -> str:
        """Returns the SQL query string."""
        return self._query

    @property
    def parameters(self) -> tuple[Any, ...]:
        """Ensures parameters are returned in an expected sequence type, specifically a tuple."""
        return self._parameters
