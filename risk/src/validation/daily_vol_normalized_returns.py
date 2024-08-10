from typing import cast
import pandas as pd
from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp

from common.src.utils.convertors import convert_dataframe_to_series, convert_dict_to_dataframe


class DailyvolNormalizedReturns(DataFrameModel):
    date_time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    returns: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_api_to_series(cls, items: dict) -> pd.Series:
        # Convert the dictionary to a DataFrame using convert_dict_to_dataframe
        data = convert_dict_to_dataframe(
            items,
            str(DailyvolNormalizedReturns.date_time),
            str(DailyvolNormalizedReturns.returns)
        )

        # Validate the DataFrame according to the schema defined in the class
        validated_data = cls.validate(data)

        # Cast the validated data back to a DataFrame
        data_frame = cast(pd.DataFrame, validated_data)

        # Convert the DataFrame to a Series using convert_dataframe_to_series
        series = convert_dataframe_to_series(
            data_frame,
            str(DailyvolNormalizedReturns.date_time),
            str(DailyvolNormalizedReturns.returns)
        )

        return series
