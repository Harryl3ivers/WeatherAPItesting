import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

def initialise_db(db_path="weather.db"):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                temperature REAL NOT NULL,
                feels_like REAL NOT NULL,
                humidity INTEGER NOT NULL,
                wind_speed REAL NOT NULL,
                condition TEXT NOT NULL,
                description TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
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
def fetch_weather_history(
    city: str,
    *,
    db_path: str = "weather.db",
    limit: int = 10
):
    """
    city: str → positional
    db_path: str → keyword-only
    limit: int → keyword-only
    """
    initialise_db(db_path)

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, city, country, temperature, feels_like, humidity,
                   wind_speed, condition, description, timestamp, recorded_at
            FROM weather_history
            WHERE LOWER(city) = LOWER(?)
            ORDER BY id DESC
            LIMIT ?
        """, (city, limit))
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "city": r[1],
                "country": r[2],
                "temperature": r[3],
                "feels_like": r[4],
                "humidity": r[5],
                "wind_speed": r[6],
                "condition": r[7],
                "description": r[8],
                "timestamp": r[9],
                "recorded_at": r[10],
            }
            for r in rows
        ]
    finally:
        conn.close()

def temperature_statistics(city: str, db_path: str = "weather.db") -> Dict[str, Any]:
    conn = sqlite3.connect("weather.db")
    try:
        cursor = conn.cursor()
        cursor.execute(""" 
                       SELECT
                       AVG(temperature) AS avg_temp,
                       MIN(temperature) AS min_temp,
                        MAX(temperature) AS max_temp
                       COUNT(*) AS record_count
                       FROM weather_history
                       WHERE LOWER(city) = LOWER(?)
                       """, (city,))
        row = cursor.fetchone()
        if row and row[3] > 0:
            return {
                "average_temperature": row[0],
                "minimum_temperature": row[1],
                "maximum_temperature": row[2],
                "record_count": row[3]
            }
        return None
    finally:
        conn.close()



     
        

    

        
        
        
        