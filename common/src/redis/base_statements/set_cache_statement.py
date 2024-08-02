class SetCacheStatement:
    def __inti__(self, cache_key, cache_value, time_to_live):
        self.cache_key = cache_key
        self.cache_value = cache_value
        self.time_to_live = time_to_live

    def get_cache_key(self):
        return self.cache_key

    def get_cache_value(self):
        return self.cache_value

    def get_time_to_live(self):
        return self.time_to_live
