# import pytest
# import pandas as pd
# from shared.src.rules.ewmac import EWMAComputer

# time_series_data = pd.Series([137.75, 138.00, 139.25])
# speed = 16
# expected_ewmac = pd.Series([0, 0.005859, 0.047608])
# input_data = {"instrument": "test_CORN", "raw_data": time_series_data}


# def test_compute_ewmac_valid_input():
#     ewmac_computer = EWMAComputer(input_data, speed)
#     ewmac = ewmac_computer.compute_ewmac()
#     assert ewmac.round(6).equals(expected_ewmac.round(6))


# def test_compute_ewmac_empty_time_series():
#     empty_input_data = {"instrument": "test_CORN", "raw_data": pd.Series()}
#     with pytest.raises(ValueError):
#         EWMAComputer(empty_input_data, speed)


# def test_compute_ewmac_negative_speed():
#     with pytest.raises(ValueError):
#         EWMAComputer(input_data, -2)


# def test_process_data_valid_input():
#     ewmac_computer = EWMAComputer(input_data, speed)
#     result = ewmac_computer.process_data()
#     assert result["instrument"] == input_data["instrument"]
#     assert result["speed"] == speed


# def test_process_data_invalid_input():
#     with pytest.raises(KeyError):
#         EWMAComputer({}, speed)
