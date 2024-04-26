import pandas as pd

from risk.src.estimators.instrument_currency_volatility import InstrumentCurrencyVolEstimator


def load_csv_data(filename):
    filepath = f"risk/tests/test_data/{filename}.csv"
    data = pd.read_csv(filepath)

    return pd.Series(data["price"])


def test_instrument_volatility():
    # Load input and expected data
    multiple_prices = load_csv_data("multiple_price")
    daily_returns_vol = load_csv_data("expected_daily_returns_volatility")
    exptected = load_csv_data("expected_instrument_vol")
    estimator = InstrumentCurrencyVolEstimator()
    calculated_vol = estimator.get_instrument_currency_vol(multiple_prices, daily_returns_vol, point_size=200)
    pd.testing.assert_series_equal(
        calculated_vol,
        exptected,
        check_dtype=True,
        rtol=1e-5,
        atol=1e-5,
        check_index_type="equiv",
        obj="CalculatedVol",
    )
