from common.database.base_statements.fetch_statement import FetchStatement


class GetAssetClass(FetchStatement):
    def __init__(self, symbol: str):
        self._query = """
        SELECT asset_class
        FROM instrument_config
        WHERE symbol = $1
        """
        self._parameters = (symbol,)

    @property
    def parameters(self) -> tuple:
        """
        Returns the parameters to be used in the SQL query.

        :return: A tuple containing the parameters.
        """
        return self._parameters
