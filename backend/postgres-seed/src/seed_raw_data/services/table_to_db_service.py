"""
bla bla
"""
from src.csv_io.services.csv_files_service import CsvFilesService

class TableToDBService:
    """
    bla bla
    """

    def __init__(self):
        self.csv_service = CsvFilesService()

    async def insert_data_from_csv_to_table_async(self, directory, table):
        """
        Asynchronously insert data from a CSV file to a database table.

        Args:
            directory (str): The directory where the CSV file is located.
            table (str): The name of the database table to insert data into.

        Returns:
            None
        """
        csv_files = self.csv_service.load_csv_files_from_directory_async(directory)

        # Step 3: Add data preprocessing using either an existing method or Pydantic
        # TODO

        # Step 4: Integrate the existing insert_dataframe_async method
        # TODO

        # Step 5: Implement error handling and logging
        # TODO

        pass
