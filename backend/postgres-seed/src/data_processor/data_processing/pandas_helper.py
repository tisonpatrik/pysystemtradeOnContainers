import pandas as pd
from typing import List
from src.csv_io.schemas.csv_output import CsvOutput


def convert_to_dataframe(csv_outputs: List[CsvOutput]) -> pd.DataFrame:
    # Initialize an empty DataFrame
    main_df = pd.DataFrame()

    for csv_output in csv_outputs:
        # Convert the data list to a DataFrame
        temp_df = pd.DataFrame(csv_output.data)

        # Add a new column to store the table name
        temp_df["table"] = csv_output.table

        # Concatenate this DataFrame to the main DataFrame
        main_df = pd.concat([main_df, temp_df], ignore_index=True)

    return main_df
