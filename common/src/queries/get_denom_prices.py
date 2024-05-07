from common.src.queries.base_statements.fetch_statement import FetchStatement


class GetDenomPriceQuery(FetchStatement):
    def __init__(self, symbol: str):
        self._query = """
        SELECT date_time, price 
        FROM multiple_prices 
        WHERE symbol = $1
        ORDER BY date_time
        """
        self._parameters = symbol

    @property
    def query(self) -> str:
        return self._query

    @property
    def parameters(self) -> str:
        return self._parameters
