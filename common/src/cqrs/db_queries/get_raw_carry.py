from common.src.database.base_statements.fetch_statement import FetchStatement


class GetRawCarryDataQuery(FetchStatement):
    def __init__(self, symbol: str):
        self._query = """
           SELECT date_time, price, carry, price_contract, carry_contract
           FROM multiple_prices
           WHERE symbol = $1
           ORDER BY date_time
           """
        self._parameters = (symbol,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
