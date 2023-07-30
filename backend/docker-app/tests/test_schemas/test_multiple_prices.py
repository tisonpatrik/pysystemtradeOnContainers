import pytest
from pydantic import ValidationError

from src.schemas.multiple_prices import MultiplePricesCreate


def test_multiple_prices_instance_empty():
    with pytest.raises(expected_exception=ValidationError):
        MultiplePricesCreate()


def test_multiple_prices_instance_amount_empty():
    with pytest.raises(expected_exception=ValidationError):
        MultiplePricesCreate(description="Description")


def test_multiple_prices_instance_description_empty():
    with pytest.raises(expected_exception=ValidationError):
        MultiplePricesCreate(amount=10)


def test_multiple_prices_instance_amount_wrong():
    with pytest.raises(expected_exception=ValidationError):
        MultiplePricesCreate(amount="amount", description="Description")
