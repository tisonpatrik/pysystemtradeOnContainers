import pandas as pd
from src.estimators.normalised_price_for_asset_class import NormalisedPriceForAssetClass


def load_csv_data(filename):
    filepath = f"data_management/tests/test_data/{filename}.csv"
    data = pd.read_csv(filepath, index_col="index")
    return pd.Series(data["price"], name="price")


def test_normalised_price_for_asset_class():
    # Load input and expected data
    instrument_cumulative_normalised_prices = load_csv_data(
        "exptected_cum_norm_returns"
    )
    normalised_price_for_asset_class = load_csv_data(
        "expected_daily_vol_normalised_returns_for_list_of_instruments"
    )
    expected = load_csv_data("expected_normalised_price_for_asset_class_aligned")

    estimator = NormalisedPriceForAssetClass()
    calculated_vol = estimator.get_normalised_price_for_asset_class(
        instrument_cumulative_normalised_price=instrument_cumulative_normalised_prices,
        normalised_price_for_asset_class=normalised_price_for_asset_class,
    )
    pd.testing.assert_series_equal(
        calculated_vol,
        expected,
        check_dtype=True,
        rtol=1e-3,
        atol=1e-3,
        check_index_type="equiv",
        check_names=False,
        obj="CalculatedVol",
    )
