from common.database.base_statements.fetch_statement import FetchStatement


class GetCarryDataQuery(FetchStatement):
    def __init__(self, symbol: str):
        super().__init__()
        self._query = """
           SELECT time, price, carry, price_contract, carry_contract
           FROM multiple_prices
           WHERE symbol = $1
           """
        self._parameters = (symbol,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
