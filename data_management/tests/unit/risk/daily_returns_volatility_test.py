import pandas as pd
import pytest
from src.risk.estimators.daily_returns_volatility import DailyReturnsVolEstimator


def load_csv_data(filename):
    filepath = f"tests/test_data/{filename}.csv"
    data = pd.read_csv(filepath)
    return pd.Series(data["price"])


def test_daily_returns():
    # Load input and expected data
    daily_prices = load_csv_data("daily_prices")
    expected_vol = load_csv_data("expected_daily_returns")

    estimator = DailyReturnsVolEstimator()
    calculated_vol = estimator.daily_returns(daily_prices)

    pd.testing.assert_series_equal(
        calculated_vol,
        expected_vol,
        check_dtype=True,
        rtol=1e-5,
        atol=1e-5,
        check_index_type="equiv",
        obj="CalculatedVol",
    )


def test_process_daily_returns_vol_exception():
    estimator = DailyReturnsVolEstimator()
    invalid_daily_prices = pd.Series(["a", "b", "c"])
    with pytest.raises(ValueError) as exc_info:
        estimator.process_daily_returns_vol(invalid_daily_prices)

    assert "General error processing daily returns volatility" in str(exc_info.value)


def test_process_daily_returns_vol():
    # Load input and expected data
    daily_prices = load_csv_data("daily_prices")
    expected_vol = load_csv_data("expected_daily_returns_vol")

    estimator = DailyReturnsVolEstimator()
    calculated_vol = estimator.process_daily_returns_vol(daily_prices)

    pd.testing.assert_series_equal(
        calculated_vol,
        expected_vol,
        check_dtype=True,
        rtol=1e-5,
        atol=1e-5,
        check_index_type="equiv",
        obj="CalculatedVol",
    )
