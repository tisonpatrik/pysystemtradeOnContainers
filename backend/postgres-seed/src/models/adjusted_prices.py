from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AdjustedPrices(Base):
    __tablename__ = "adjusted_prices"

    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    price = Column(Float)
