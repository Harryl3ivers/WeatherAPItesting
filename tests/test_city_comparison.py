from main.city_comparison import MultiCityComparison
import pytest
from unittest.mock import patch, MagicMock

class TestMultiCityComparison:
    @patch("main.city_comparison.WeatherClient")
    def test_compare_cities(self, mock_get):
        mock_client = MagicMock()

    # THIS is the equivalent of json.return_value
        mock_client.weather_data.side_effect = [
        {
            "city": "London",
            "temperature": 15.0,
            "country": "GB"
        },
        {
            "city": "New York",
            "temperature": 20.0,
            "country": "US"
        }
    ]

        mock_get.return_value = mock_client

        comparison = MultiCityComparison()
        result = comparison.compare_cities(["London", "New York"], "metric")

        assert result[0]["city"] == "London"
        assert result[1]["city"] == "New York"
        
         



    
    def test_compare_cities_empty_list(self):
        comparison = MultiCityComparison()
        with pytest.raises(ValueError,match="City list cannot be empty"):
            comparison.compare_cities([],"metric")
    
    def test_compare_cities_exceed_max(self):
        compariosn = MultiCityComparison()
        cities = [f"City{i}" for i in range(11)]
        with pytest.raises(ValueError,match="Maximum allowed cities is 10"):
            compariosn.compare_cities(cities,"metric")
    
    @patch("main.city_comparison.WeatherClient")
    def test_get_hottest_cities(self,mock_get):
        mock_client = MagicMock()
        mock_client.get_current_weather.return_value = {}
        mock_client.weather_data.side_effect = [
            {
            "city": "London",
            "temperature": 15.0,
            "country": "GB"
        },
        {
            "city": "New York",
            "temperature": 20.0,
            "country": "US"
        },
        {
            "city": "Cairo",
            "temperature": 30.0,
            "country": "EG"
        }

        ]
        mock_get.return_value = mock_client
        comparison = MultiCityComparison()
        hottest = comparison.get_hottest_cities(["London","New York","Cairo"],"metric")
        assert hottest["city"] == "Cairo" 

    @patch("main.city_comparison.WeatherClient")
    def test_get_coldest_city(self,mock_get):
        mock_client = MagicMock()
        mock_client.get_current_weather.return_value = {}
        mock_client.weather_data.side_effect = [
            {
            "city": "London",
            "temperature": 15.0,
            "country": "GB"
        },
        {
            "city": "New York",
            "temperature": 20.0,
            "country": "US"
        },
        {
            "city": "Cairo",
            "temperature": 30.0,
            "country": "EG"
        }

        ]
        mock_get.return_value = mock_client
        comparison = MultiCityComparison()
        coldest = comparison.get_coldest_city(["London","New York","Cairo"],"metric")
        assert coldest["city"] == "London"
    
    @patch("main.city_comparison.WeatherClient")
    def test_get_average_temperature(self,mock_get):
        mock_client = MagicMock()
        mock_client.get_current_weather.return_value = {}
        mock_client.weather_data.side_effect = [
            {
            "city": "London",
            "temperature": 15.0,
            "country": "GB"
        },
        {
            "city": "New York",
            "temperature": 20.0,
            "country": "US"
        },
        {
            "city": "Cairo",
            "temperature": 25.0,
            "country": "EG"
        }
        ]
        mock_get.return_value = mock_client
        comaparison = MultiCityComparison()
        average = comaparison.get_average_temperature(["London","New York","Cairo"],"metric")
        assert average == 20.0
    

         




