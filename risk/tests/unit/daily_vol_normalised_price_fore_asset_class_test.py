import pandas as pd

from risk.src.estimators.daily_vol_normalised_returns_for_asset_class import (
    DailyVolNormalisedPriceForAssetClassEstimator,
)


def load_csv_series(filename):
    filepath = "risk/tests/test_data/{filename}.csv"
    data = pd.read_csv(filepath)
    return pd.Series(data["price"])


def load_csv_dataframes(filename):
    filepath = f"risk/tests/test_data/{filename}.csv"
    data = pd.read_csv(filepath)
    return pd.DataFrame(data)


def test_daily_returns():
    # Load input and expected data
    daily_prices = load_csv_dataframes("aggregate_returns_across_instruments")
    expected_vol = load_csv_series("expected_daily_vol_normalised_returns_for_list_of_instruments")

    estimator = DailyVolNormalisedPriceForAssetClassEstimator()
    calculated_vol = estimator.aggregate_daily_vol_normalised_returns_for_list_of_instruments(daily_prices)
    pd.testing.assert_series_equal(
        calculated_vol,
        expected_vol,
        check_dtype=True,
        rtol=1e-5,
        atol=1e-5,
        check_names=False,
        check_index_type="equiv",
        obj="CalculatedVol",
    )
