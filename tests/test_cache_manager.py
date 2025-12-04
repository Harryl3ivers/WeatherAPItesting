import pytest 
import time 
from main.cache_manager import CacheManager
from freezegun import freeze_time



class TestCacheManager:
    def test_cache_initialization(self):
        cache = CacheManager()
        assert cache.cache == {}
        assert cache.expiration_time == 300
        assert cache.hits == 0
        assert cache.misses == 0
    
    def test_set_and_get(self):
        """Test basic set and get operations"""
        cache = CacheManager()
        cache.set("key1", "value1")
        
        result = cache.get("key1")
        assert result == "value1"

    def test_get_nonexistent_key(self):
        cache = CacheManager()
        result = cache.get("nonexistent")
        assert result is None
        assert cache.misses == 1
    
    def test_cache_stores_different_types(self):
        cache = cache = CacheManager()
        cache.set("int", 42)
        cache.set("list", [1, 2, 3])
        cache.set("dict", {"a": 1})
        assert cache.get("int") == 42
        assert cache.get("list") == [1, 2, 3]
        assert cache.get("dict") == {"a": 1}


    @freeze_time("2025-04-12 10:00:00")
    def test_expiration(self):
        cache = CacheManager()
        cache.set("temp_key", "temp_value")
        # Move time forward by 301 seconds to expire the cache
        with freeze_time("2025-04-12 10:05:01"):
            result = cache.get("temp_key")
            assert result is None
            assert cache.misses == 1
    
    def test_overwrite_cache(self):
        cache = CacheManager()
        cache.set("key", "value1")
        cache.set("key", "value2")
        assert cache.get("key") == "value2"
    
    def test_delete_key(self):
        cache = CacheManager()
        cache.set("key", "value")
        cache.delete("key")
        assert cache.get("key") is None
    
    def test_delete_nonexistent_key(self):
        cache = CacheManager()
        # Should not raise an error
        cache.delete("nonexistent")
    
    def test_clear_cache(self):
        cache = CacheManager()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None
        stats = cache.get_stats()
        assert stats['hits'] == 0
        assert stats['misses'] == 2
    
    def test_cache_hit_tracking(self):
        cache = CacheManager()
        cache.set("key", "value")
        cache.get("key")
        stats = cache.get_stats()
        assert stats['hits'] == 1
        assert stats['misses'] == 0

    
    def test_cache_miss_tracking(self):
        cache = CacheManager()
        cache.get("nonexistent")
        cache.get("nonexistent2")
        stats = cache.get_stats()
        assert stats['hits'] == 0
        assert stats['misses'] == 2
    
    def test_cache_size_tracking(self):
        cache = CacheManager()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        stats = cache.get_stats()
        assert stats['size'] == 2

    @freeze_time("2025-04-12 10:00:00")
    def test_expired_items_removed_upon_accessing(self):
        """Test that expired items are removed when accessed"""
        cache = CacheManager()
        cache.set("key1", "value1")
        with freeze_time("2025-04-12 10:05:01"):
            result = cache.get("key1")
            assert result is None
            stats = cache.get_stats()
            assert stats['size'] == 0




        