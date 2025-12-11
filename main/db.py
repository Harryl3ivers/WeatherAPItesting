import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

def initialise_db(db_path = "weather.db"):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS weather_history ("""
                       "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "city TEXT NOT NULL, "
                       "country TEXT NOT NULL, "
                       "temperature REAL NOT NULL, "
                          "feels_like REAL NOT NULL, "
                          "humidity INTEGER NOT NULL, "
                            "wind_speed REAL NOT NULL, "
                            "condition TEXT NOT NULL,  "
                            "description TEXT NOT NULL, "
                            "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"
                            "recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP"
                       )
        conn.commit()
    finally:
        conn.close()

def save_weather_data(db_path: str = "weather.db", weather: Optional[Dict[str, Any]] = None):
    if weather is None:
        weather = {}

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO weather_history 
            (id, city, country, temperature, feels_like, humidity, wind_speed, condition, description, timestamp, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            weather.get("id"),
            weather.get("city"),
            weather.get("country"),
            weather.get("temperature"),
            weather.get("feels_like"),
            weather.get("humidity"),
            weather.get("wind_speed"),
            weather.get("condition"),
            weather.get("description"),
            weather.get("timestamp"),
            datetime.now()  # recorded_at
        ))
        conn.commit()   
    finally:
        conn.close()
def fetch_weather_history(db_path: str = "weather.db", limit: int = 10) -> List[Dict[str, Any]]:
    pass

        
        
        
        