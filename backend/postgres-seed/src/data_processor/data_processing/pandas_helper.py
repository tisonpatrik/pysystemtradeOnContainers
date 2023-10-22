"""
bla
"""

import logging
import pandas as pd
from typing import List
from src.data_processor.errors.data_processing_errors import ColumnRenameError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def convert_to_dataframe() -> pd.DataFrame:
#     """
#     Convert a list of CsvOutput objects to a single concatenated DataFrame.

#     Parameters:
#         csv_outputs: List of CsvOutput objects containing path, table name, and data.

#     Returns:
#         pd.DataFrame: A DataFrame containing the concatenated data and table names.

#     Raises:
#         ColumnRenameError: If renaming columns fails.
#     """
#     try:
#         # Initialize an empty DataFrame
#         main_df = pd.DataFrame()

#         for csv_output in csv_outputs:
#             # Convert the data list to a DataFrame
#             temp_df = pd.DataFrame(csv_output.data)

#             # Add a new column to store the table name
#             temp_df["table"] = csv_output.table

#             # Concatenate this DataFrame to the main DataFrame
#             main_df = pd.concat([main_df, temp_df], ignore_index=True)

#         logger.info("Successfully converted CsvOutputs to DataFrame.")

#     except Exception as e:
#         logger.error("Failed to convert CsvOutputs to DataFrame: %s", e)
#         raise ColumnRenameError(f"Failed to rename columns: {e}") from e

#     return main_df


def rename_columns(data_frame, new_column_names):
    """
    Renames DataFrame columns based on the provided dictionary.
    """
    missing_columns = set(new_column_names.keys()) - set(data_frame.columns)
    if missing_columns:
        missing_columns_str = ", ".join(missing_columns)
        logger.error("Columns %s do not exist in the DataFrame", missing_columns_str)
        raise ColumnRenameError(f"Columns {missing_columns_str} do not exist")
    try:
        return data_frame.rename(columns=new_column_names)
    except Exception as error:
        logger.error("Error during column renaming: %s", error)
        raise ColumnRenameError from error
