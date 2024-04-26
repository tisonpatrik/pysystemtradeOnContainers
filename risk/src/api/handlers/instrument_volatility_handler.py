import pandas as pd

from common.src.database.repository import Repository
from common.src.database.statements.fetch_statement import FetchStatement
from common.src.logging.logger import AppLogger
from risk.src.api.models.queries import AvaragePositionQuery


class InstrumentVolHandler:
    def __init__(self, repository: Repository) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def get_instrument_vol_for_symbol_async(self, postition_query: AvaragePositionQuery) -> pd.Series:
        query = "SELECT date_time, instrument_volatility FROM instrument_volatility WHERE symbol = $1"
        statement = FetchStatement(query=query, parameters=postition_query.symbol)
        instrument_volatility = await self.repository.fetch_many_async(statement)
        df = pd.DataFrame(instrument_volatility)
        instr_value_vol = pd.Series(data=df["instrument_volatility"].values, index=pd.to_datetime(df["date_time"]))
        vol_scalar = postition_query.annual_cash_vol_target / instr_value_vol
        print(instr_value_vol.tail())
        return vol_scalar

        # instr_ccy_vol = self.get_instrument_currency_vol(symbol)
        # fx_rate = self.get_fx_rate(symbol)
        # fx_rate = pd.Series([1.0] * len(instr_ccy_vol), index=instr_ccy_vol.index)  # Mocking fx_rate

        # fx_rate = fx_rate.reindex(instr_ccy_vol.index, method="ffill")

        # instr_value_vol = instr_ccy_vol.ffill() * fx_rate

    # def get_instrument_currency_vol(self, instrument_code: str):

    #     block_value = self.get_block_value(instrument_code)
    #     daily_perc_vol = self.get_price_volatility(instrument_code)

    #     ## FIXME WHY NOT RESAMPLE?
    #     (block_value, daily_perc_vol) = block_value.align(daily_perc_vol, join="inner")

    #     instr_ccy_vol = block_value.ffill() * daily_perc_vol

    #     return instr_ccy_vol
