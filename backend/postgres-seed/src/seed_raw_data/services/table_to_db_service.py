"""
Handles the service logic for mapping various tables to the database. 
Responsible for orchestrating the flow of data from raw files to processed data in the database.
"""
import logging
from typing import List
from src.seed_raw_data.schemas.data_frame_container import DataFrameContainer
from src.seed_raw_data.errors.table_to_db_errors import InvalidFileNameError, ProcessingError
from src.data_processor.services.instrumentconfig_service import InstrumentConfigService
from src.data_processor.services.moreinstrumentinfo_service import MoreInstrumentInfoService
from src.data_processor.services.rollconfig_service import RollConfigService
from src.data_processor.services.spreadcost_service import SpreadCostService
from src.data_processor.services.adjustedprices_service import AdjustedPricesService
from src.data_processor.services.fxprices_service import FxPricesService
from src.data_processor.services.multipleprices_service import MultiplePricesService
from src.data_processor.services.rollcalendars_service import RollCalendarsService
from src.seed_raw_data.schemas.files_mapping import FileTableMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TableToDBService:
    """
    Manages the conversion of raw data files to processed data for various services.
    Aggregates processed data and routes it to the appropriate database tables.
    """

    def __init__(self):
        self.instrumentconfig_service = InstrumentConfigService()
        self.moreinstrumentinfo_service = MoreInstrumentInfoService()
        self.rollconfig_service = RollConfigService()
        self.spreadcost_service = SpreadCostService()
        self.adjustedprices_service = AdjustedPricesService()
        self.fxprices_service = FxPricesService()
        self.multipleprices_service = MultiplePricesService()
        self.rollcalendars_service = RollCalendarsService()


    async def get_processed_data_from_raw_files(self, map_items: List[FileTableMapping])-> List[DataFrameContainer]:
        """
        Orchestrates the processing of raw data files and their conversion to database-friendly formats.
        Iterates over a list of FileTableMapping items and processes each according to its file_name attribute.
        """
        logger.info("Data processing for csv files has started")
        processed_data = []
        for map_item in map_items:
            try:
                result = await self._process_map_item(map_item)
                if result:
                    processed_data.append(result)
            
            except InvalidFileNameError as e:
                logger.error("Encountered an error with file name: %s", map_item.file_name, exc_info=True)
            except ProcessingError as e:
                logger.error("Processing failed for file: %s", map_item.file_name, exc_info=True)
            except Exception as e:
                logger.exception("An unexpected error occurred: %s", e)
        return processed_data

    async def _process_map_item(self, map_item: FileTableMapping):
        """
        Processes individual FileTableMapping item based on its table attribute.

        Args:
            map_item (FileTableMapping): The object containing mapping information for file processing.

        Returns:
            DataFrameContainer: Processed data for the table or None if not applicable.
        """
        if map_item.table == 'instrument_config':
            return self.instrumentconfig_service.process_instrument_config(map_item)
        elif map_item.table == 'instrument_metadata':
            return await self.moreinstrumentinfo_service.process_more_instrument_info(map_item)
        elif map_item.table == 'roll_config':
            return await self.rollconfig_service.process_roll_config(map_item)
        elif map_item.table == 'spread_cost':
            return await self.spreadcost_service.process_spread_cost(map_item)
        elif map_item.table == 'adjusted_prices':
            return await self.adjustedprices_service.process_adjusted_prices(map_item)
        elif map_item.table == 'fx_prices':
            return await self.fxprices_service.process_fx_prices(map_item)
        elif map_item.table == 'multiple_prices':
            return await self.multipleprices_service.process_multiple_prices(map_item)
        elif map_item.table == 'roll_calendars':
            return await self.rollcalendars_service.process_roll_calendars(map_item)
        else:
            return None
