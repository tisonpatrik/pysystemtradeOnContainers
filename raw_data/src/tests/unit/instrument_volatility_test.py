import pandas as pd

from raw_data.services.instrument_currency_vol_service import InstrumentCurrencyVolService


def load_csv_data(filename: str) -> pd.Series:
    filepath = f"raw_data/tests/test_data/{filename}.csv"
    data = pd.read_csv(filepath)
    return data["price"]


def test_instrument_volatility():
    # Load input and expected data
    multiple_prices = load_csv_data("multiple_price")
    daily_returns_vol = load_csv_data("daily_returns_volatility")
    expected = load_csv_data("instrument_vol")

    estimator = InstrumentCurrencyVolService()
    calculated_vol = estimator.calculate_instrument_vol_async(multiple_prices, daily_returns_vol, point_size=200)

    # Ensure both are pd.Series
    assert isinstance(calculated_vol, pd.Series), "calculated_vol is not a pd.Series"
    assert isinstance(expected, pd.Series), "expected is not a pd.Series"

    # Compare the series
    pd.testing.assert_series_equal(
        calculated_vol,
        expected,
        check_dtype=True,
        rtol=1e-5,
        atol=1e-5,
        check_index_type="equiv",
        obj="CalculatedVol",
    )
