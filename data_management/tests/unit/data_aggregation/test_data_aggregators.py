# import pandas as pd
# import pytest
# from pandas.testing import assert_frame_equal

# from src.common_utils.errors.aggregation_errors import DataAggregationError
# from src.raw_data.utils.data_aggregators import (
#     aggregate_to_day_based_prices,
#     concatenate_data_frames,
# )


# @pytest.fixture
# def time_based_dataframe():
#     df = pd.DataFrame(
#         {
#             "date_time": [
#                 "2021-01-01 12:00:00",
#                 "2021-01-01 14:00:00",
#                 "2021-01-02 12:00:00",
#             ],
#             "price": [100.0, 110.0, 105.0],
#         }
#     )
#     df["date_time"] = pd.to_datetime(df["date_time"])
#     return df


# # Test with a DataFrame that has multiple entries for a single day.
# def test_aggregate_to_day_based_prices_single_day_multiple_entries(
#     time_based_dataframe,
# ):
#     # Adding extra data to the fixture for a single day
#     extra_data = pd.DataFrame(
#         {
#             "date_time": ["2021-01-01 16:00:00", "2021-01-01 18:00:00"],
#             "price": [120.0, 130.0],
#         }
#     )
#     extra_data["date_time"] = pd.to_datetime(extra_data["date_time"])
#     test_df = pd.concat([time_based_dataframe, extra_data], ignore_index=True)

#     expected_result = pd.DataFrame(
#         {
#             "date_time": ["2021-01-01", "2021-01-02"],
#             "price": [(100 + 110 + 120 + 130) / 4, 105],
#         }
#     )
#     expected_result["date_time"] = pd.to_datetime(expected_result["date_time"])

#     result = aggregate_to_day_based_prices(test_df, "date_time")

#     assert_frame_equal(result, expected_result)


# # Test with already aggerated.
# def test_aggregate_to_day_based_prices_already_daily():
#     # Define the DataFrame that already consists of daily data
#     test_df = pd.DataFrame(
#         {"date_time": ["2021-01-01", "2021-01-02"], "price": [100, 105]}
#     )
#     test_df["date_time"] = pd.to_datetime(test_df["date_time"])

#     expected_result = test_df.copy().astype(
#         {"price": "float64"}
#     )  # Update dtype to float64

#     result = aggregate_to_day_based_prices(test_df, "date_time")

#     assert_frame_equal(result, expected_result)


# # Test with invalid date_time_column input.
# def test_aggregate_to_day_based_prices_invalid_datetime_column(time_based_dataframe):
#     # Intentionally providing an incorrect datetime column name
#     invalid_column_name = "invalid_column"

#     with pytest.raises(DataAggregationError):
#         aggregate_to_day_based_prices(time_based_dataframe, invalid_column_name)


# # Test with empty DataFrame
# def test_aggregate_to_day_based_prices_empty_dataframe():
#     # Create an empty DataFrame
#     empty_dataframe = pd.DataFrame()

#     with pytest.raises(DataAggregationError):
#         aggregate_to_day_based_prices(empty_dataframe, "DATETIME")


# @pytest.fixture
# def sample_data_frames():
#     df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
#     df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
#     return [df1, df2]


# # Test for a successful concatenation
# def test_concatenate_data_frames_success(sample_data_frames):
#     expected_df = pd.DataFrame({"A": [1, 2, 5, 6], "B": [3, 4, 7, 8]})
#     result_df = concatenate_data_frames(sample_data_frames)
#     pd.testing.assert_frame_equal(result_df, expected_df)
