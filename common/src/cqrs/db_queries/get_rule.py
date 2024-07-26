from common.src.database.base_statements.fetch_statement import FetchStatement


class GetAllRules(FetchStatement):
    def __init__(self) -> None:
        self._query = """
		SELECT name, speed
		FROM rules
		"""

    @property
    def parameters(self) -> tuple:
        """
        Returns the parameters to be used in the SQL query.

        :return: A tuple containing the parameters.
        """
        return ()
