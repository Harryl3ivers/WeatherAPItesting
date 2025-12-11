from weather_client import WeatherClient
from cache_manager import CacheManager
from rate_limiter import RateLimiter
import logging
import sys
from validator import validator
class WeatherCLI:
    def __init__(self):
        self.cache = CacheManager()  # Cache expiration time in seconds
        self.client = WeatherClient()
        self.rate_limiter = RateLimiter(max_requests=60, period_seconds=60)
         

    def main(self):
        print("Welcome to the Weather CLI!")
        print("=" * 30)

        while True:
            print("\nOptions:")
            print("1. Get current weather by city name")
            print("2. Get current weather by coordinates")
            print("3. View cache statistics")
            print("4. Exit")
        
            choice = input("Enter your choice (1-3): ").strip()

            if choice == "1":
             self.get_current_city()
            elif choice == "2":
                self.get_current_coordinates()
            elif choice == "3":
                self.display_cache_stats()
            elif choice == "4":
                print("Exiting the Weather CLI. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

    
    def get_current_city(self):
        city = input("Enter city namae: ").strip()
        try:
            city = validator.valid_city(city)
            units = input("Enter units (metric/imperial): ").strip()
            units = validator.valid_units(units)

            cache_key = f"city:{city}:units:{units}"
            cached_weather = self.cache.get(cache_key)
           
            if cached_weather:
                logging.info("Fetching weather data from cache.")
                self._display_weather(cached_weather)
                return
            
            if not self.rate_limiter.allow_request():
                print("Rate limit exceeded. Please try again later.")
                status = self.rate_limiter.get_status()
                logging.info(f"Rate Limiter Status: {status}")
                return
            weather = self.client.get_current_weather(city=city, units=units)
            parsed = self.client.weather_data(weather)

            #store in cache
            self.cache.set(cache_key, parsed)
            self._display_weather(parsed)

            print(f"Current weather in {city} {units}:")
            print(weather)
        except Exception as e:
            print(f"Error fetching weather data: {e}")

    def get_current_coordinates(self):
        lattude = input("Enter latitude: ").strip()
        longitude = input("Enter longitude: ").strip()
        units = input("Enter units (metric/imperial): ").strip()
        units = validator.valid_units(units)
        try:
            lattude, longitude = validator.valid_coordinates(lattude, longitude)
            weather_cords = self.client.get_weather_by_coordinates(lat=lattude, lon=longitude, units=units)
            print(f"Current weather at coordinates ({lattude}, {longitude}) ({units}):")
            print(weather_cords)
        except Exception as e:
            print(f"Error fetching weather data: {e}")
    
    def display_cache_stats(self):
        stats = self.cache.get_stats()
        print("\nCache Statistics:")
        print(f"  Hits: {stats['hits']}")
        print(f"  Misses: {stats['misses']}")
        print(f"  Current Size: {stats['size']} items")

    def _display_weather(self, weather):
        """Pretty print weather data"""
        print(f"\n {weather['city']}, {weather['country']}")
        print(f"  Temperature: {weather['temperature']:.1f}°C (feels like {weather['feels_like']:.1f}°C)")
        print(f" Humidity: {weather['humidity']}%")
        print(f"  Wind: {weather['wind_speed']} m/s")
        print(f"  Conditions: {weather['description']}")

if __name__ == "__main__":
    WeatherCLI().main()