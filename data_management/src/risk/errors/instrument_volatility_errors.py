class InstrumentVolatilityProcessingError(Exception):
    """Exception raised for errors in the processing of instrument volatility."""


class InstrumentVolatilityCalculationError(Exception):
    """Exception raised for errors in calculating instrument volatility."""


class VolatilityProcessingHaltedError(Exception):
    """Exception raised when volatility processing is halted due to an error."""
