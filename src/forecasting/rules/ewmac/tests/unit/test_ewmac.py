import pytest
import pandas as pd
from ewmac_rule import compute_ewmac, process_data, lambda_handler

time_series_data = pd.Series([137.75, 138.00, 139.25])
speed = 16
expected_ewmac = pd.Series([0, 0.005859, 0.047608])

def test_compute_ewmac_valid_input():    
    
    ewmac = compute_ewmac(time_series_data, speed)
    assert ewmac.round(6).equals(expected_ewmac.round(6))

def test_compute_ewmac_empty_time_series():
    time_series_data = pd.Series()
    speed = 2

    with pytest.raises(ValueError):
        compute_ewmac(time_series_data, speed)

def test_compute_ewmac_negative_speed():
    time_series_data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    speed = -2

    with pytest.raises(ValueError):
        compute_ewmac(time_series_data, speed)

def test_process_data_valid_input():
    test_instrument = 'test_CORN'
    input_data = {
        'instrument': test_instrument,
        'speed': speed,
        'raw_data': time_series_data
    }
    result = process_data(input_data)
    assert result['instrument'] == test_instrument
    assert result['speed'] == speed

def test_process_data_invalid_input():
    with pytest.raises(KeyError):
        process_data({})
