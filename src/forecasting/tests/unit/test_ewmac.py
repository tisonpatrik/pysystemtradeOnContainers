import pytest
import pandas as pd
from ewmac.ewmac_rule import compute_ewmac

def test_compute_ewmac_valid_input():
    time_series_data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    speed = 2
    expected_ewmac = pd.Series(
        [
            0.0, 0.66666667, 1.25, 1.78571429, 2.29411765, 2.77777778, 3.24137931, 3.68965517, 4.12643678, 4.55555556
        ]
    )

    ewmac = compute_ewmac(time_series_data, speed)
    assert ewmac.round(8).equals(expected_ewmac.round(8))

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

