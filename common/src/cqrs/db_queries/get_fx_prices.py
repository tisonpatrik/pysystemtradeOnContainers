from common.src.database.base_statements.fetch_statement import FetchStatement


class GetDailyFxPrices(FetchStatement):
    def __init__(self, fx_code: str):
        self._query = """
        SELECT day_bucket, last_price
        FROM daily_fx_prices
        WHERE symbol = $1
        """
        self._parameters = (fx_code,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
