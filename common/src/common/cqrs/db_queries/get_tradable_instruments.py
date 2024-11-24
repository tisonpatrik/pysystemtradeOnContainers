from common.database.base_statements.fetch_statement import FetchStatement


class GetTradableInstruments(FetchStatement):
    def __init__(self, is_tradable: bool):
        self._query = """
        SELECT symbol
        FROM instrument_config
        WHERE  is_tradable = $1
        ORDER BY symbol ASC;
        """
        self._parameters = (is_tradable,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
