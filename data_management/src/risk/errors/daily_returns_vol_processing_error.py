class DailyReturnsVolProcessingError(Exception):
    """Exception raised for errors in the processing of daily returns volatility."""


class DailyReturnsVolCalculationError(Exception):
    """Exception raised for errors in calculating daily returns volatility."""


class DailyReturnsVolProcessingHaltedError(Exception):
    """Exception raised when daily returns volatility processing is halted due to an error."""


class DailyReturnsVolatilityFetchError(Exception):
    """Exception raised for errors in fetching daily returns volatility."""
