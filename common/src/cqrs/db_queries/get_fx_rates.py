from common.src.database.base_statements.fetch_statement import FetchStatement


class GetFxRatesQuery(FetchStatement):
    def __init__(self, symbol: str):
        self._query = """
        SELECT time, price
        FROM fx_prices
        WHERE symbol = $1
        """
        self._parameters = (symbol,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
