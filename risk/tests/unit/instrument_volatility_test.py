import pandas as pd

from risk.src.services.instrument_currency_vol_service import InstrumentCurrencyVolService


def load_csv_data(filename):
    filepath = f"risk/tests/test_data/{filename}.csv"
    data = pd.read_csv(filepath)

    return pd.Series(data["price"])


def test_instrument_volatility():
    # Load input and expected data
    multiple_prices = load_csv_data("multiple_price")
    daily_returns_vol = load_csv_data("daily_returns_volatility")
    exptected = load_csv_data("expected_instrument_vol")
    estimator = InstrumentCurrencyVolService()
    calculated_vol = estimator.calculate_instrument_vol_async(multiple_prices, daily_returns_vol, point_size=200)
    pd.testing.assert_series_equal(
        calculated_vol,
        exptected,
        check_dtype=True,
        rtol=1e-5,
        atol=1e-5,
        check_index_type="equiv",
        obj="CalculatedVol",
    )
