from common.src.database.base_statements.insert_statement import InsertStatement
from common.src.validation.rule import Rule


class CreateRule(InsertStatement):
    """Class for creating rules, inherits from InsertStatement."""

    def __init__(self, data: Rule):
        self.table_name = "rules"
        super().__init__(self.table_name, data)
