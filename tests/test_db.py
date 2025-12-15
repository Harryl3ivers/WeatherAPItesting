import pytest
import sqlite3
from main.db import initialise_db, save_weather_data, fetch_weather_history
from datetime import datetime, timedelta
import os

@pytest.fixture
def db_path():
    test_db_path = "test_weather.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)  # Ensure a clean state before each test
    
    initialise_db(test_db_path) 
    yield test_db_path
    if os.path.exists(test_db_path):
        os.remove(test_db_path)  # Clean up after tests

class TestWeatherDB:
    def test_init_db(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            """SELECT name FROM sqlite_master WHERE type="table" AND name="weather_history";"""
        )
        table = cursor.fetchone()
        conn.close()
        assert table[0] == "weather_history"
    
    def test_save_weather(self, db_path):
        weather = {
            "city": "London",
            "country": "GB",
            "temperature": 15.5,
            "feels_like": 14.2,
            "humidity": 72,
            "pressure": 1013,
            "wind_speed": 3.5,
             "condition":"clouds",
            "description": "cloudy",
            "timestamp": 1234567890
        }
        save_weather_data(db_path,weather)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM weather_history""")
        rows = cursor.fetchall()
        conn.close()

        assert len(rows) == 1
        assert rows[0][1] == "London"

    def test_save_weather_multiple_records(self,db_path):
        weather1 = {
            'city': 'London',
            'country': 'GB',
            'temperature': 15.5,
            'feels_like': 14.2,
            'humidity': 72,
            'wind_speed': 3.5,
            "condition":"clouds",
            'description': 'cloudy'
        }
        
        weather2 = {
            'city': 'Paris',
            'country': 'FR',
            'temperature': 18.0,
            'feels_like': 17.5,
            'humidity': 65,
            'wind_speed': 2.1,
            "condition":"sunny",
            'description': 'sunny'
        }
        save_weather_data(db_path,weather1)
        save_weather_data(db_path,weather2)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM weather_history""")
        rows = cursor.fetchall()
        conn.close()
        assert len(rows) == 2
        assert rows[0][1] == ('London')
        assert rows[1][1] == ('Paris')
    
    def test_get_city_history(self,db_path):
        weather = {
            'city': 'Paris',
            'country': 'FR',
            'temperature': 18.0,
            'feels_like': 17.5,
            'humidity': 65,
            'wind_speed': 2.1,
            "condition":"sunny",
            'description': 'sunny'
        }
        save_weather_data(db_path,weather)
        history = fetch_weather_history("Paris",db_path)
        assert len(history) ==1
        assert history[0]["city"] == "Paris"
    
    def test_get_city_history_case_insensitive(self, db_path):
        pass