from src.db.tables.business_data_tables.raw_adjusted_prices_table import AdjustedPricesTableBase

# Define the table model
class AdjustedPricesTable(AdjustedPricesTableBase, table=True):
    __tablename__ = "adjusted_prices"
