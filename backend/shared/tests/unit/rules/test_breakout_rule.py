# import pytest
# import pandas as pd
# import numpy as np
# from shared.src.rules.breakout import BreakoutComputer

# time_series_data = pd.Series([137.75, 138.00, 139.25])
# speed = 4
# expected_breakdown = pd.Series([np.nan, 20, 20])
# input_data = {"instrument": "test_CORN", "raw_data": time_series_data}

# def test_compute_breakdown_valid_input():
#     breakout_computer = BreakoutComputer(input_data, speed)
#     breakdown = breakout_computer.compute_breakdown()
#     assert breakdown.round(6).equals(expected_breakdown.round(6))

# def test_compute_breakdown_empty_time_series():
#     empty_input_data = {
#         'instrument': 'test_CORN',
#         'raw_data': pd.Series()
#     }
#     with pytest.raises(ValueError):
#         BreakoutComputer(empty_input_data, speed)

# def test_compute_breakdown_negative_speed():
#     with pytest.raises(ValueError):
#         BreakoutComputer(input_data, -2)

# def test_process_data_valid_input():
#     breakout_computer = BreakoutComputer(input_data, speed)
#     result = breakout_computer.process_data()
#     assert result['instrument'] == input_data['instrument']
#     assert result['speed'] == speed

# def test_process_data_invalid_input():
#     with pytest.raises(KeyError):
#         BreakoutComputer({}, speed)
