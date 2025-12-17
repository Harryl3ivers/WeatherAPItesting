import sys
import logging

from weather_client import WeatherClient
from cache_manager import CacheManager
from rate_limiter import RateLimiter
from db import (
    initialise_db,
    save_weather_data,
    fetch_weather_history,
    temperature_statistics,
)
from validator import validator


class WeatherCLI:
    def __init__(self):
        self.cache = CacheManager()
        self.client = WeatherClient()
        self.rate_limiter = RateLimiter(max_requests=60, period_seconds=60)
        initialise_db()

    def main(self):
        print("Welcome to the Weather CLI!")
        print("=" * 30)

        while True:
            print("\nOptions:")
            print("1. Get current weather by city name")
            print("2. Get current weather by coordinates")
            print("3. View cache statistics")
            print("4. View weather history for a city")
            print("5. View temperature stats for a city")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                self.get_current_city()
            elif choice == "2":
                self.get_current_coordinates()
            elif choice == "3":
                self.display_cache_stats()
            elif choice == "4":
                self.view_history()
            elif choice == "5":
                self.view_stats()
            elif choice == "6":
                print("Exiting the Weather CLI. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

    def get_current_city(self):
        city = input("Enter city name: ").strip()

        try:
            city = validator.valid_city(city)
            units = validator.valid_units(
                input("Enter units (metric/imperial): ").strip()
            )

            cache_key = f"city:{city}:units:{units}"
            cached_weather = self.cache.get(cache_key)

            if cached_weather:
                logging.info("Fetching weather data from cache.")
                self._display_weather(cached_weather)
                return

            if not self.rate_limiter.allow_request():
                print("Rate limit exceeded. Please try again later.")
                return

            raw_weather = self.client.get_current_weather(city=city, units=units)
            parsed_weather = self.client.weather_data(raw_weather)

            self.cache.set(cache_key, parsed_weather)
            save_weather_data(parsed_weather)

            self._display_weather(parsed_weather)

        except Exception as e:
            print(f"Error fetching weather data: {e}")

    def get_current_coordinates(self):
        latitude = input("Enter latitude: ").strip()
        longitude = input("Enter longitude: ").strip()

        try:
            latitude, longitude = validator.valid_coordinates(latitude, longitude)
            units = validator.valid_units(
                input("Enter units (metric/imperial): ").strip()
            )

            if not self.rate_limiter.allow_request():
                print("Rate limit exceeded. Please try again later.")
                return

            raw_weather = self.client.get_weather_by_coordinates(
                lat=latitude,
                lon=longitude,
                units=units,
            )

            parsed_weather = self.client.weather_data(raw_weather)
            self._display_weather(parsed_weather)

        except Exception as e:
            print(f"Error fetching weather data: {e}")

    def view_history(self):
        city = input("Enter city name: ").strip()

        try:
            city = validator.valid_city(city)
            history = fetch_weather_history(city, limit=10)

            if not history:
                print(f"No history found for {city}")
                return

            print(f"\nLast 10 weather records for {city}")
            print("-" * 70)

            for record in history:
                print(
                    f"{record['recorded_at'][:19]} | "
                    f"{record['temperature']:.1f}°C | "
                    f"{record['description']}"
                )

        except Exception as e:
            print(f"Error: {e}")

    def view_stats(self):
        city = input("Enter city name: ").strip()

        try:
            city = validator.valid_city(city)
            stats = temperature_statistics(city)

            if not stats:
                print(f"No statistics found for {city}")
                return

            print(f"\nTemperature statistics for {city}")
            print("-" * 70)
            print(f"Average: {stats['avg_temp']:.1f}°C")
            print(f"Minimum: {stats['min_temp']:.1f}°C")
            print(f"Maximum: {stats['max_temp']:.1f}°C")
            print(f"Records: {stats['record_count']}")

        except Exception as e:
            print(f"Error: {e}")

    def display_cache_stats(self):
        stats = self.cache.get_stats()

        print("\nCache Statistics:")
        print(f"Hits: {stats['hits']}")
        print(f"Misses: {stats['misses']}")
        print(f"Current size: {stats['size']} items")

    def _display_weather(self, weather):
        print(f"\n{weather['city']}, {weather['country']}")
        print(
            f"Temperature: {weather['temperature']:.1f}°C "
            f"(feels like {weather['feels_like']:.1f}°C)"
        )
        print(f"Humidity: {weather['humidity']}%")
        print(f"Wind: {weather['wind_speed']} m/s")
        print(f"Conditions: {weather['description']}")


if __name__ == "__main__":
    WeatherCLI().main()
