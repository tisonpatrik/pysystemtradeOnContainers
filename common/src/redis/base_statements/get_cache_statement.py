class GetCacheStatement:
    """Abstract class for encapsulating data fetching key for Redis.
    This class must be extended with specific implementations that format or validate queries."""

    def __init__(self, key):
        self._key = key

    @property
    def key(self):
        return self._key
