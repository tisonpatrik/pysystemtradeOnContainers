import pytest
import pandas as pd
from src.data_processor.data_processing import pandas_helper


# Mock logger for testing
class MockLogger:
    def error(self, *args):
        pass


logger = MockLogger()


def test_convert_to_dataframe(mock_csv_outputs):
    # Execute function
    result_df = pandas_helper.convert_to_dataframe(mock_csv_outputs)

    # Build expected DataFrame
    expected_data = {
        "col1": ["value11", "value21", "value31", "value41"],
        "col2": ["value12", "value22", "value32", "value42"],
        "table": ["table1", "table1", "table2", "table2"],
    }
    expected_df = pd.DataFrame(expected_data)

    # Verify DataFrame
    pd.testing.assert_frame_equal(result_df, expected_df)
