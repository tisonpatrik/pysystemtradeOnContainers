class DailyReturnsVolSeedingError(Exception):
    """Exception raised for errors in the seeding of daily returns volatility."""


class InstrumentVolSeedingError(Exception):
    """Exception raised for errors in seeding instrument volatility."""


class CumulativeVolatilityReturnsSeedingError(Exception):
    """Exception raised for errors in seeding cumulative volatility returns."""


class NormalisedPriceForAssetSeedError(Exception):
    """Exception raised for errors in seeding normalised prices for asset class."""
