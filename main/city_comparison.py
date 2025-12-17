from main.weather_client import WeatherClient
from main.validator import validator
from main.cache_manager import CacheManager
from main.rate_limiter import RateLimiter


class MultiCityComparison:
    def __init__(self,db_path = "weather.db"):
        self.client = WeatherClient()
        self.validator = validator()
        self.cache = CacheManager(ttl_seconds = 300)
        self.rate_limiter = RateLimiter(max_requests=60,period_seconds=60)
    
    def compare_cities(self,cities,units):
        units = self.validator.valid_units(units)
        validated_city = []
        for city in cities:
            try: