from common.database.base_statements.fetch_statement import FetchStatement


class GetAllRules(FetchStatement):
    def __init__(self) -> None:
        self._query = """
		SELECT rule_variation_name, rule_name, rule_parameters, scaling_factor, use_attenuation
		FROM rules
		"""

    @property
    def parameters(self) -> tuple:
        """
        Returns the parameters to be used in the SQL query.

        :return: A tuple containing the parameters.
        """
        return ()
