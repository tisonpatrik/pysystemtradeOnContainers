import pandas as pd
from src.raw_data.utils.csv_loader import load_csv
from src.raw_data.utils.path_validator import get_full_path
from src.common_utils.utils.rename_columns import rename_columns
from src.raw_data.schemas.files_mapping import FileTableMapping


def process_config_files_table(map_item: FileTableMapping) -> pd.DataFrame:
    """
    Reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object.
    """
    full_path = get_full_path(map_item.directory, map_item.file_name)
    raw_data = load_csv(full_path)
    renamed = rename_columns(raw_data, map_item.columns_mapping)
    return renamed