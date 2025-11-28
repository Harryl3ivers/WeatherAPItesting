import requests
import os
from dotenv import load_dotenv

class WeatherClient:
    BaseUrl = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("WEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("Api key not found. Set the Weather api key in the .env file.")
    
    def get_current_weather(self, city="London",units="metric"):
        url = f"{self.BaseUrl}?q=London&appid={self.api_key}&units=metric"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
         
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
        data = response.json()
        return data

    def get_weather_by_coordinates(self, lat, lon, units="metric"):
        url = f"{self.BaseUrl}?lat={lat}&lon={lon}&appid={self.api_key}&units={units}"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": units,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
        data = response.json()
        return data
     