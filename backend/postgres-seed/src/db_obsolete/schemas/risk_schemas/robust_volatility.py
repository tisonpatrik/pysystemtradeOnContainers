

class RobustVolatility():

    @property
    def sql_command(self):
        """
        Returns the SQL command to create the 'robust_volatility' table.

        Returns:
            str: SQL command string.
        """
        return """
                CREATE TABLE robust_volatility (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        volatility FLOAT,
                        PRIMARY KEY (unix_date_time, symbol)
                    )
                """

    @property
    def table_name(self):
        """
        Returns the name of the 'robust_volatility' database table.

        Returns:
            str: Name of the database table.
        """
        return "robust_volatility"