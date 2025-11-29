import pytest
from unittest.mock import patch, MagicMock
from main.weather_client import WeatherClient

class TestWeatherClient:
    @patch("main.weather_client.requests.get")
    def test_get_current_weather(self, mock_get):
        # Mocked API response
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

        # Assert the raw API response has expected values
        assert weather["name"] == "London"
        assert weather["sys"]["country"] == "GB"
        assert weather["main"]["temp"] == 15.0
        assert weather["weather"][0]["description"] == "light rain"
        assert weather["wind"]["speed"] == 5.0
        assert weather["coord"]["lat"] == 51.51
        assert weather["coord"]["lon"] == -0.13
