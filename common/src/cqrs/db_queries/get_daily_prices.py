from common.src.database.base_statements.fetch_statement import FetchStatement


class GetDailyPriceQuery(FetchStatement):
    def __init__(self, symbol: str):
        self._query = """
        SELECT day_bucket, last_price
        FROM daily_adjusted_prices
        WHERE symbol = $1
        """
        self._parameters = (symbol,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
