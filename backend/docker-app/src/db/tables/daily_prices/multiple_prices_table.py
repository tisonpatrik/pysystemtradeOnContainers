from src.db.tables.business_data_tables.raw_multiple_prices_table import MultiplePricesTableBase


# Define the table model
class MultiplePricesTable(MultiplePricesTableBase, table=True):
    __tablename__ = "multiple_prices"