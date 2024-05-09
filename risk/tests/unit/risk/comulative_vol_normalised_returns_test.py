import pandas as pd

from risk.src.services.cumulative_daily_vol_normalised_returns_service import (
	CumulativeDailyVolatilityNormalisedReturnsService,
)


def load_input_data():
	filepath = f'risk/tests/test_data/expected_norm_return.csv'
	data = pd.read_csv(filepath)
	data.columns = ['date_time', 'vol_normalized_returns']
	data['date_time'] = pd.to_datetime(data['date_time'])
	data = data.set_index('date_time')
	return data


def load_expected_data():
	filepath = f'risk/tests/test_data/exptected_cum_norm_returns.csv'
	data = pd.read_csv(filepath)
	data.columns = ['date_time', 'cum_vol_norm_returns']
	data['date_time'] = pd.to_datetime(data['date_time'])
	data = data.set_index('date_time')
	return data


def test_cumulative_vol_normalized_returns():
	# Load input and expected data
	input = load_input_data()
	expected = load_expected_data()

	service = CumulativeDailyVolatilityNormalisedReturnsService()
	calculated_vol = service.calculate_cumulative_vol_for_prices(input)
	pd.testing.assert_frame_equal(
		calculated_vol,
		expected,
		check_dtype=True,
		rtol=1e-5,
		atol=1e-5,
		check_index_type='equiv',
		obj='CalculatedVol',
	)
