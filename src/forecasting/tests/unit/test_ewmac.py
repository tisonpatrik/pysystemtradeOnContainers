import unittest
from unittest.mock import AsyncMock, patch
import pandas as pd
import numpy as np
from ewmac import compute_ewmac, compute_and_save_ewmac, process_record
from aws_lambda_powertools.utilities.data_classes import SQSRecord

class TestHandler(unittest.TestCase):

    def test_compute_ewmac(self):
        time_series_data = pd.Series([100, 101, 102, 101, 100])
        speed = 2
        ewmac = compute_ewmac(time_series_data, speed)
        expected_ewmac = pd.Series([0.0, 0.5, 1.0, 0.6666666666666661, 0.4285714285714284])
        pd.testing.assert_series_equal(ewmac, expected_ewmac, atol=1e-6)

    @patch("handler.get_time_series_from_dynamodb", new_callable=AsyncMock)
    @patch("handler.write_daily_prices", new_callable=AsyncMock)
    async def test_compute_and_save_ewmac(self, mock_write_daily_prices, mock_get_time_series_from_dynamodb):
        instrument = "TEST"
        speed = 2
        time_series_data = pd.Series([100, 101, 102, 101, 100])
        mock_get_time_series_from_dynamodb.return_value = time_series_data
        ewmac = await compute_and_save_ewmac(instrument, speed)

        mock_get_time_series_from_dynamodb.assert_called_once_with("RAW_DATA_TABLE", instrument)
        mock_write_daily_prices.assert_called_once()
        self.assertEqual(len(ewmac), 5)

    async def test_process_record(self):
        with patch("handler.compute_and_save_ewmac", new_callable=AsyncMock) as mock_compute_and_save_ewmac:
            mock_compute_and_save_ewmac.return_value = np.array([0, 0.5, 1, 0.6667, 0.4286])

            record_data = {
                "body": {
                    "instrument": "TEST",
                    "speed": 2
                }
            }
            record = SQSRecord(record_data)

            result = await process_record(record)

            self.assertEqual(result["message"], "EWMAC calculation and save completed successfully")
            self.assertEqual(result["rule"], "MAC")
            self.assertEqual(result["instrument"], "TEST")
            self.assertEqual(result["speed"], 2)

if __name__ == '__main__':
    unittest.main()
