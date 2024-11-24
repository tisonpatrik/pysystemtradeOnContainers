from common.cqrs.db_queries.get_all_instruments import GetAllInstruments
from common.cqrs.db_queries.get_all_instruments_for_asset_class import GetAllInstrumentsForAssetClass
from common.cqrs.db_queries.get_asset_class import GetAssetClass
from common.cqrs.db_queries.get_instrument_currency import GetInstrumentCurrency
from common.cqrs.db_queries.get_point_size import GetPointSize
from common.cqrs.db_queries.get_tradable_instruments import GetTradableInstruments
from common.cqrs.db_queries.get_tradable_instruments_for_asset_class import GetTradableInstrumentsForAssetClass
from common.database.repository import PostgresClient
from common.logging.logger import AppLogger
from common.utils.convertors import to_pydantic
from common.validation.asset_class import AssetClass
from common.validation.instrument import Instrument
from common.validation.instrument_currency import InstrumentCurrency
from common.validation.point_size import PointSize


class InstrumentsClient:
    def __init__(self, repository: PostgresClient):
        self.repository = repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_point_size_async(self, symbol: str) -> float:
        statement = GetPointSize(symbol=symbol)
        point_size_data = await self.repository.fetch_item_async(statement)
        point_size = to_pydantic(point_size_data, PointSize)
        if point_size is None:
            raise ValueError(f"No data found for symbol {symbol}")
        return point_size.pointsize

    async def get_asset_class_async(self, symbol: str) -> str:
        statement = GetAssetClass(symbol=symbol)
        asset_class_data = await self.repository.fetch_item_async(statement)
        asset_class = to_pydantic(asset_class_data, AssetClass)
        if asset_class is None:
            raise ValueError(f"No data found for symbol {symbol}")
        return asset_class.asset_class

    async def get_tradable_instruments_for_asset_class_async(self, asset_class: str) -> list:
        statement = GetTradableInstrumentsForAssetClass(asset_class=asset_class, is_tradable=True)
        instruments_data = await self.repository.fetch_many_async(statement)
        if instruments_data is None:
            raise ValueError(f"No data found for asset_class {asset_class}")
        return [to_pydantic(instrument, Instrument) for instrument in instruments_data]

    async def get_all_instruments_for_asset_class_async(self, asset_class: str) -> list:
        statement = GetAllInstrumentsForAssetClass(asset_class=asset_class)
        instruments_data = await self.repository.fetch_many_async(statement)
        if instruments_data is None:
            raise ValueError(f"No data found for asset_class {asset_class}")
        return [to_pydantic(instrument, Instrument) for instrument in instruments_data]

    async def get_tradable_instrument_async(self) -> list:
        statement = GetTradableInstruments(is_tradable=True)
        instruments_data = await self.repository.fetch_many_async(statement)
        if instruments_data is None:
            raise ValueError("No data found for tradable instruments ")
        return [to_pydantic(instrument, Instrument) for instrument in instruments_data]

    async def get_all_instrument_async(self) -> list:
        statement = GetAllInstruments()
        instruments_data = await self.repository.fetch_many_async(statement)
        if instruments_data is None:
            raise ValueError("No data found for instruments ")
        return [to_pydantic(instrument, Instrument) for instrument in instruments_data]

    async def get_instrument_currency_async(self, symbol: str) -> InstrumentCurrency:
        statement = GetInstrumentCurrency(symbol=symbol)
        currency_data = await self.repository.fetch_item_async(statement)
        currency = to_pydantic(currency_data, InstrumentCurrency)
        if currency is None:
            raise ValueError(f"No data found for symbol {symbol}")
        return currency
