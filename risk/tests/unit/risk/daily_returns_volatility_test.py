import pandas as pd

from risk.src.estimators.daily_vol_normalised_returns import DailyVolNormalisedReturns


def load_csv_data(filename):
	filepath = f'risk/tests/test_data/{filename}.csv'
	data = pd.read_csv(filepath)
	return pd.Series(data['price'].astype(float))


def test_daily_returns():
	# Load input and expected data
	daily_prices = load_csv_data('daily_prices')
	expected_vol = load_csv_data('expected_daily_returns')

	estimator = DailyVolNormalisedReturns()
	calculated_vol = estimator.daily_returns(daily_prices)

	pd.testing.assert_series_equal(
		calculated_vol,
		expected_vol,
		check_dtype=True,
		rtol=1e-5,
		atol=1e-5,
		check_index_type='equiv',
		obj='CalculatedVol',
	)


def test_process_daily_returns_vol():
	# Load input and expected data
	daily_prices = load_csv_data('daily_prices')
	expected_vol = load_csv_data('expected_daily_returns_volatility')

	estimator = DailyVolNormalisedReturns()
	calculated_vol = estimator.process_daily_returns_vol(daily_prices)

	pd.testing.assert_series_equal(
		calculated_vol,
		expected_vol,
		check_dtype=True,
		rtol=1e-5,
		atol=1e-5,
		check_index_type='equiv',
		obj='CalculatedVol',
	)
