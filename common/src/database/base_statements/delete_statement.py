from pydantic import BaseModel


class DeleteStatement:
    """Statement class for preparing a single object for delete operations."""

    def __init__(self, table_name: str, condition: BaseModel):
        self._table_name = table_name
        self._condition = condition

    def get_columns(self) -> list[str]:
        """Returns a list of column names from the condition."""
        return list(self._condition.model_dump().keys())

    def get_values(self) -> list:
        """Returns a list of values from the condition."""
        return list(self._condition.model_dump().values())
