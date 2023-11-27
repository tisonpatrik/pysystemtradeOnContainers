class CumulativeVolatilityReturnsCalculationError(Exception):
    """Exception raised for errors in calculating cumulative volatility returns."""


class CumulativeVolatilityReturnsProcessingError(Exception):
    """Exception raised for errors in processing cumulative volatility returns."""


class CumulativeVolatilityReturnsProcessingHaltedError(Exception):
    """Exception raised when the processing of cumulative volatility returns is halted due to an error."""
