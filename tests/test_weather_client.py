import pytest
from unittest.mock import patch, MagicMock
from main.weather_client import WeatherClient

class TestWeatherClient:
    @patch("main.weather_client.requests.get")
    def test_get_current_weather(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "London",
            "sys": {"country": "GB"},
            "main": {
                "temp": 15.0,
                "feels_like": 13.0,
                "humidity": 80
            },
            "wind": {"speed": 5.0},
            "weather": [{"description": "light rain"}],
            "coord": {"lat": 51.51, "lon": -0.13}
        }

        mock_get.return_value = mock_response

        client = WeatherClient()
        weather = client.get_current_weather(city="London", units="metric")
        assert weather["name"] == "London"
        assert weather["sys"]["country"] == "GB"
        assert weather["main"]["temp"] == 15.0
        assert weather["weather"][0]["description"] == "light rain"
        assert weather["wind"]["speed"] == 5.0
        assert weather["coord"]["lat"] == 51.51
        assert weather["coord"]["lon"] == -0.13
    
    @patch("main.weather_client.requests.get")
    def test_get_weather_by_coordinates(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
              "name": "London",
            "sys": {"country": "GB"},
            "main": {
                "temp": 15.0,
                "feels_like": 13.0,
                "humidity": 80
            },
            "wind": {"speed": 5.0},
            "weather": [{"description": "light rain"}],
            "coord": {"lat": 51.51, "lon": -0.13}
        }
        mock_get.return_value = mock_response
        client = WeatherClient()
        weather = client.get_weather_by_coordinates(lat=51.51, lon=-0.13, units="metric")
        assert weather["name"] == "London"
        assert weather["coord"]["lat"] == 51.51
        assert weather["coord"]["lon"] == -0.13
    
    @patch("main.weather_client.requests.get")
    def test_city_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("404 Client Error: Not Found for url")
        mock_get.return_value = mock_response

    @patch("main.weather_client.requests.get")
    def test_invalid_api_key(self,mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("401 Client Error")
        mock_get.return_value = mock_response
        
    @patch("main.weather_client.requests.get")
    def test_missing_api_key(self,mock_get):
        mock_get.side_effect = KeyError("API key not found")
        client = WeatherClient()
        with pytest.raises(KeyError):
            client.get_current_weather(city="London", units="metric")

    
    @patch("main.weather_client.requests.get")
    def test_missing_weather_description(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "London",
            "sys": {"country": "GB"},
            "main": {
                "temp": 15.0,
                "feels_like": 13.0,
                "humidity": 80
            },
            "wind": {"speed": 5.0},
            "weather": [],
            "coord": {"lat": 51.51, "lon": -0.13}
        }
        mock_get.return_value = mock_response
        client = WeatherClient()
        weather = client.get_current_weather(city="London", units="metric")
        assert weather["weather"] == []