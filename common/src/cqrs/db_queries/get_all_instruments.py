from common.src.database.base_statements.fetch_statement import FetchStatement


class GetAllInstruments(FetchStatement):
    def __init__(self) -> None:
        self._query = """
        SELECT symbol
        FROM instrument_config
        ORDER BY symbol ASC;
        """

    @property
    def parameters(self) -> tuple:
        """
        Returns the parameters to be used in the SQL query.

        :return: A tuple containing the parameters.
        """
        return ()
