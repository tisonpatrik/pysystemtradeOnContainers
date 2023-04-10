import pytest
import pandas as pd
from ewmac.ewmac_rule import compute_ewmac

def test_compute_ewmac_valid_input():
    time_series_data = pd.Series([137.75, 138.00, 139.25])
    speed = 16
    expected_ewmac = pd.Series(
        [
            0, 0.005859, 0.047608
        ]
    )
    ewmac = compute_ewmac(time_series_data, speed)
    assert ewmac.round(6).equals(expected_ewmac.round(6))

def test_compute_ewmac_empty_time_series():
    time_series_data = pd.Series([])
    speed = 2

    with pytest.raises(ValueError):
        compute_ewmac(time_series_data, speed)

def test_compute_ewmac_negative_speed():
    time_series_data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    speed = -2

    with pytest.raises(ValueError):
        compute_ewmac(time_series_data, speed)

