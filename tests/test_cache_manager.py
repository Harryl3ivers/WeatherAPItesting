import pytest 
import time 
from main.cache_manager import CacheManager
# import freezegun

class TestCacheManager:
    def test_cache_initialization(self):
        cache = CacheManager()
        assert cache.cache == {}
        assert cache.expiration_time == 300
        assert cache.hits == 0
        assert cache.misses == 0