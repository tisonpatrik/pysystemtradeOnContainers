import pandas as pd
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def convert_series_to_frame(series: pd.Series) -> pd.DataFrame:
    """
    Converts a Pandas Series to a Pandas DataFrame.
    """
    try:
        # Convert the Series to a DataFrame first
        data_frame = series.reset_index()
        return data_frame

    except Exception as exc:
        error_message = f"An error occurred during conversion {str(exc)}"
        logger.error(error_message)
        raise ValueError(error_message)
