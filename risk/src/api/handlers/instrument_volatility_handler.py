from common.src.logging.logger import AppLogger


class InstrumenmtVolatilityHandler:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    async def get_instrument_vol_for_symbol_async(self, instrument_code: str):
        return "hello"
        # instr_ccy_vol = self.get_instrument_currency_vol(instrument_code)
        # fx_rate = self.get_fx_rate(instrument_code)

        # fx_rate = fx_rate.reindex(instr_ccy_vol.index, method="ffill")

        # instr_value_vol = instr_ccy_vol.ffill() * fx_rate

        # return instr_value_vol
