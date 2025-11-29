from weather_client import WeatherClient
import sys
from validator import validator
class WeatherCLI:
    def __init__(self):
        self.client = WeatherClient()

    def main(self):
        print("Welcome to the Weather CLI!")
        print("=" * 30)

        while True:
            print("\nOptions:")
            print("1. Get current weather by city name")
            print("2. Get current weather by coordinates")
            print("3. Exit")
        
            choice = input("Enter your choice (1-3): ").strip()

            if choice == "1":
             self.get_current_city()
            elif choice == "2":
                self.get_current_coordinates()
            elif choice == "3":
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
            weather = self.client.get_current_weather(city=city)
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
            weather_cords = self.client.get_weather_by_coordinates(lat=lattude, lon=longitude)
            print(f"Current weather at coordinates ({lattude}, {longitude}) ({units}):")
            print(weather_cords)
        except Exception as e:
            print(f"Error fetching weather data: {e}")

    def _display_weather(self, weather):
        """Pretty print weather data"""
        print(f"\n {weather['city']}, {weather['country']}")
        print(f"  Temperature: {weather['temperature']:.1f}°C (feels like {weather['feels_like']:.1f}°C)")
        print(f" Humidity: {weather['humidity']}%")
        print(f"  Wind: {weather['wind_speed']} m/s")
        print(f"  Conditions: {weather['description']}")

if __name__ == "__main__":
    WeatherCLI().main()