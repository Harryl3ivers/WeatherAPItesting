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
        if not cities:
            raise ValueError("City list cannot be empty")
        if len(cities) > 10:
            raise ValueError("Maximum allowed cities is 10")
        units = self.validator.valid_units(units)
        results = []
        for city in cities:
            try:
                validated_city = self.validator.valid_city(city) #Clean and validate the city name.
                cache_key = f"{validated_city} : {units}"
                cached = self.cache.get(cache_key)
                if cached:
                     results.append(cached)
                     continue
                weather = self.client.get_current_weather(validated_city,units)
                parsed = self.client.weather_data(weather)
                self.cache.set(cache_key,parsed)
                results.append(parsed)
            except Exception as e:
                raise ValueError
            return results
    
    def get_hottest_cities(self,cities,units):
        results = self.compare_cities(cities,units)
        valid = [city for city in results if "error" not in city]
        if not valid:
            raise ValueError("No valid weather data found")
        return max(valid,key=lambda city:city["temperature"])


                  
                
