import pytest
import asyncio
from pandas import DataFrame
from unittest.mock import MagicMock
from app import compute_ewmac, process_record

@pytest.fixture
def time_series_data():
    return DataFrame({"price": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]})

@pytest.fixture
def ewmac_config(monkeypatch):
    monkeypatch.setenv("RAW_DATA_TABLE", "raw_data_table")
    monkeypatch.setenv("RAW_FORECAST_TABLE", "raw_forecast_table")

@pytest.mark.asyncio
async def test_compute_ewmac(time_series_data):
    speed = 2
    expected_ewmac = [0.0, 5.0, 9.285714285714285, 12.857142857142858, 16.153846153846153, 19.23076923076923, 22.12121212121212, 24.848484848484848, 27.430555555555554, 29.88392857142857]
    ewmac = compute_ewmac(time_series_data, speed)

    assert len(ewmac) == len(expected_ewmac)
    assert all(abs(a - b) < 1e-9 for a, b in zip(ewmac, expected_ewmac))

@pytest.mark.asyncio
async def test_process_record(ewmac_config):
    record = MagicMock()
    record.body = {
        "instrument": "TEST",
        "speed": 2
    }

    with pytest.patch("forecasting.src.ewmac.ewmac.compute_and_save_ewmac", new=MagicMock()) as mock_compute_and_save_ewmac:
        mock_compute_and_save_ewmac.return_value = asyncio.Future()
        mock_compute_and_save_ewmac.return_value.set_result([0.0, 5.0, 9.285714285714285])

        result = await process_record(record)

        mock_compute_and_save_ewmac.assert_called_once_with("TEST", 2)
        assert result == {
            'message': 'EWMAC calculation and save completed successfully',
            'rule': 'MAC',
            'instrument': 'TEST',
            'speed': 2
        }
