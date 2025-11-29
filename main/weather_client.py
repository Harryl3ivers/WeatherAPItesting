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
        url = f"{self.BaseUrl}?q=city&appid={self.api_key}&units=metric"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
         
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
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
    
    def weather_data(self, data):
        weather = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "coordinates": {
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"]
        }
    }
        return weather
