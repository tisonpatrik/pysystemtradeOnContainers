import pandas as pd
from src.estimators.daily_vol_normalised_returns import DailyVolNormalisedReturns


def load_csv_data(filename):
    filepath = f"data_management/tests/test_data/{filename}.csv"
    data = pd.read_csv(filepath)
    return pd.Series(data["price"])


def test_daily_returns():
    # Load input and expected data
    daily_prices = load_csv_data("daily_prices")
    expected_vol = load_csv_data("expected_norm_return")

    estimator = DailyVolNormalisedReturns()
    calculated_vol = estimator.get_daily_vol_normalised_returns(daily_prices)
    pd.testing.assert_series_equal(
        calculated_vol,
        expected_vol,
        check_dtype=True,
        rtol=1e-5,
        atol=1e-5,
        check_index_type="equiv",
        obj="CalculatedVol",
    )
