from common.src.database.base_statements.fetch_statement import FetchStatement


class GetAllInstruments(FetchStatement):
    def __init__(self) -> None:
        self._query = """
        SELECT symbol
        FROM instrument_config
        WHERE have_data = true
        ORDER BY symbol ASC;
        """

    @property
    def parameters(self) -> tuple:
        return ()
