from common.src.database.base_statements.fetch_statement import FetchStatement


class GetFxPrices(FetchStatement):
    def __init__(self, fx_code: str):
        self._query = """
        SELECT time, price
        FROM fx_prices
        WHERE symbol = $1
        ORDER BY time
        """
        self._parameters = (fx_code,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
