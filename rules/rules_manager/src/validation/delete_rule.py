from common.src.database.base_statements.delete_statement import DeleteStatement
from common.src.validation.rule import Rule


class DeleteRule(DeleteStatement):
    """Class for deleting rules, inherits from DeleteStatement."""

    def __init__(self, data: Rule):
        self.table_name = "rules"
        super().__init__(self.table_name, data)
