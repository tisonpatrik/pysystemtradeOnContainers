from common.src.queries.db_queries.base_statements.fetch_statement import FetchStatement


class GetDailyPriceQuery(FetchStatement):
    def __init__(self, symbol: str):
        self._query = """
        SELECT date_time, price 
        FROM adjusted_prices 
        WHERE symbol = $1
        ORDER BY date_time
        """
        self._parameters = (symbol,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
