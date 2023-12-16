class InstrumentConfigError(Exception):
    """
    Failed to get instrument_list_of_symbols_asyncnt config asynchronously: %s
    """


class InstrumentMetadataError(Exception):
    """
    Failed to get get_instrument_metadatas_async config asynchronously: %s
    """

class TradableInstrumentsError(Exception):
    """
    Failed to get get_tradable_instruments config asynchronously: %s
    """