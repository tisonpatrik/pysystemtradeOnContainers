from common.src.queries.db_queries.base_statements.fetch_statement import FetchStatement


class GetRule(FetchStatement):
	def __init__(self, name: str, speed: int) -> None:
		self._query = """
        SELECT name, speed
        FROM rules 
        WHERE name = $1 AND speed = $2
        """
		self._parameters = (name, speed)

	@property
	def parameters(self) -> tuple:
		"""
		Returns the parameters to be used in the SQL query.

		:return: A tuple containing the parameters.
		"""
		return self._parameters


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
