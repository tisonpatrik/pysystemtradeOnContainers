import pandas as pd
from src.estimators.comulative_vol_normalised_returns import (
    CumulativeVolNormalisedReturns,
)


def load_csv_data(filename):
    filepath = f"tests/test_data/{filename}.csv"
    data = pd.read_csv(filepath)
    return pd.Series(data["price"])


def test_daily_returns():
    # Load input and expected data
    input = load_csv_data("expected_norm_return")
    expected = load_csv_data("exptected_cum_norm_returns")

    estimator = CumulativeVolNormalisedReturns()
    calculated_vol = estimator.get_cumulative_daily_vol_normalised_returns(input)
    pd.testing.assert_series_equal(
        calculated_vol,
        expected,
        check_dtype=True,
        rtol=1e-5,
        atol=1e-5,
        check_index_type="equiv",
        obj="CalculatedVol",
    )
