from common.src.queries.base_statements.fetch_statement import FetchStatement


class GetInstrumentCurrency(FetchStatement):
    def __init__(self, symbol: str):
        self._query = """
        SELECT currency 
        FROM instrument_config 
        WHERE symbol = $1
        """
        self._parameters = symbol

    @property
    def query(self) -> str:
        return self._query

    @property
    def parameters(self) -> str:
        return self._parameters
