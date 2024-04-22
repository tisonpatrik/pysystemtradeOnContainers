import pandas as pd
import pytest

from risk.src.estimators.daily_returns_volatility import DailyReturnsVolEstimator


def load_csv_data(filename):
    filepath = f"risk/tests/test_data/{filename}.csv"
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
    invalid_daily_prices = pd.Series(["a", "b", "c"])  # Non-numeric input
    with pytest.raises(ValueError) as exc_info:
        estimator.process_daily_returns_vol(invalid_daily_prices)

    assert "Input must be numeric" in str(exc_info.value)  # Expect a specific error message about non-numeric input


def test_process_daily_returns_vol():
    # Load input and expected data
    daily_prices = load_csv_data("daily_prices")
    expected_vol = load_csv_data("expected_daily_returns_volatility")

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
