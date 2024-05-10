from typing import Union

import pandas as pd


class InsertStatement:
    """Statement class for preparing data for insert operations. This class accepts either a pandas DataFrame or Series."""

    def __init__(self, table_name: str, data: Union[pd.DataFrame, pd.Series]):
        self._table_name = table_name
        self._data = data

    def get_records(self):
        """Converts the data to a numpy array for insertion purposes."""
        return self._data.to_numpy()

    def get_columns(self) -> list[str]:
        """Returns a list of column names from the data."""
        return self._data.columns.tolist()

    def get_table_name(self) -> str:
        """Returns the table name."""
        return self._table_name
