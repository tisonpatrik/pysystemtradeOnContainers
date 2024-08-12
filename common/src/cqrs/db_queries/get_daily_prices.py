from common.src.database.base_statements.fetch_statement import FetchStatement


class GetDailyPriceQuery(FetchStatement):
    def __init__(self, symbol: str):
        self._query = """
        SELECT
            DATE_TRUNC('day', time) AS time,
            MAX(price) AS price
        FROM adjusted_prices
        WHERE symbol = $1
        GROUP BY DATE_TRUNC('day', time)
        ORDER BY time;
        """
        self._parameters = (symbol,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
