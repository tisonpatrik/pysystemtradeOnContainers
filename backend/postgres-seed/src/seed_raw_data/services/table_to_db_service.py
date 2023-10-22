"""
bla bla
"""
import logging
from typing import List
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
    bla bla
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


    async def get_processed_data_from_raw_files(self, map_items: List[FileTableMapping]):
        """
        bla bla
        """
        processed_data = []
        for map_item in map_items:
            if map_item.file_name == 'instrumentconfig':
                result = await self.instrumentconfig_service.process_instrument_config(map_item)
            elif map_item.file_name == 'moreinstrumentinfo':
                result = await self.moreinstrumentinfo_service.process_more_instrument_info(map_item)
            elif map_item.file_name == 'rollconfig':
                result = await self.rollconfig_service.process_roll_config(map_item)
            elif map_item.file_name == 'spread_cost':
                result = await self.spreadcost_service.process_spread_cost(map_item)
            elif map_item.file_name == 'adjusted_prices':
                result = await self.adjustedprices_service.process_adjusted_prices(map_item)
            elif map_item.file_name == 'fx_prices':
                result = await self.fxprices_service.process_fx_prices(map_item)
            elif map_item.file_name == 'multiple_prices':
                result = await self.multipleprices_service.process_multiple_prices(map_item)  
            elif map_item.file_name == 'roll_calendars':
                result = await self.rollcalendars_service.process_roll_calendars(map_item)
            else:
                result = None
            if result:
                processed_data.append(result)
        return processed_data