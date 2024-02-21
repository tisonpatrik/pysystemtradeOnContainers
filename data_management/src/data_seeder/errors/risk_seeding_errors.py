class DailyReturnsVolSeedingError(Exception):
    """Exception raised for errors in the seeding of daily returns volatility."""


class InstrumentVolSeedingError(Exception):
    """Exception raised for errors in seeding instrument volatility."""


class DailyVolatilityNormalisedReturnsSeedingError(Exception):
    """Exception raised for errors in seeding daily volatility normalised returns."""