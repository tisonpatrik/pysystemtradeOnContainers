from asyncpg.prepared_stmt import PreparedStatement


class Statement:
    def __init__(self, prepared_statement: PreparedStatement):
        self.prepared_statement = prepared_statement

    def get_statement(self):
        return self.prepared_statement

    def get_parameters(self):
        return self.prepared_statement.get_parameters()
