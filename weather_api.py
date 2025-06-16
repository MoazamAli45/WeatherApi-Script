import requests
import sqlite3
import logging
import os
from typing import List, Dict
from datetime import datetime
from config import API_KEY, WEATHER_API_URL, DATABASE_FILE, validate_api_key

# Configure logging (controlled by main.py)
logger = logging.getLogger(__name__)

class WeatherAPI:
    """Class to handle weather API interactions and data storage."""
    
    def __init__(self, timeout: int = 10):
        self.api_key = API_KEY
        self.api_url = WEATHER_API_URL
        self.database_file = DATABASE_FILE
        self.timeout = timeout
        
        if not validate_api_key(self.api_key):
            logger.error("Invalid API key provided")
            raise ValueError("Invalid API key")
        
        # Initialize SQLite database
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database and create cities and weather_data tables."""
        try:
            logger.info(f"Using database file: {os.path.abspath(self.database_file)}")
            with sqlite3.connect(self.database_file) as conn:
                cursor = conn.cursor()
                # Create cities table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cities (
                        city TEXT NOT NULL UNIQUE
                    )
                """)
                # Create weather_data table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS weather_data (
                        time TIMESTAMP NOT NULL,
                        city TEXT NOT NULL,
                        temperature REAL
                    )
                """)
                conn.commit()
                logger.info(f"Initialized SQLite database at {self.database_file}")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def read_cities(self) -> List[str]:
        """Read city names from cities table."""
        try:
            with sqlite3.connect(self.database_file) as conn:
                cursor = conn.cursor()
                # Check if cities table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cities'")
                if not cursor.fetchone():
                    logger.error("Cities table does not exist in the database")
                    return []
                
                # Read cities
                cursor.execute("SELECT city FROM cities WHERE city IS NOT NULL AND city != ''")
                cities = [row[0] for row in cursor.fetchall()]
                logger.info(f"Read {len(cities)} cities from {self.database_file}: {cities}")
                return cities
        except sqlite3.Error as e:
            logger.error(f"Error reading cities: {str(e)}")
            return []

    def add_cities(self, cities: List[str]):
        """Add cities to the cities table, ignoring duplicates."""
        try:
            with sqlite3.connect(self.database_file) as conn:
                cursor = conn.cursor()
                valid_cities = [city for city in cities if city and isinstance(city, str)]
                if not valid_cities:
                    logger.warning("No valid cities provided to add")
                    return
                cursor.executemany(
                    "INSERT OR IGNORE INTO cities (city) VALUES (?)",
                    [(city,) for city in valid_cities]
                )
                conn.commit()
                logger.info(f"Added {cursor.rowcount} new cities to {self.database_file}")
        except sqlite3.Error as e:
            logger.error(f"Error adding cities: {str(e)}")

    def fetch_weather_data(self, city: str) -> Dict:
        """Fetch weather data for a single city from WeatherAPI."""
        params = {'key': self.api_key, 'q': city, 'aqi': 'no'}
        try:
            response = requests.get(self.api_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                logger.error(f"API error for {city}: {data['error']['message']}")
                return {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'city': city, 'temperature': None}
            
            weather_info = {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city': city,
                'temperature': data['current']['temp_c']
            }
            logger.info(f"Fetched weather for {city}: {weather_info['temperature']}°C")
            return weather_info
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error(f"Unauthorized API key for {city}. Please verify your API key.")
            elif e.response.status_code == 400:
                logger.error(f"Invalid city name or query for {city}. Check city spelling.")
            else:
                logger.error(f"HTTP error fetching weather for {city}: {str(e)}")
            return {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'city': city, 'temperature': None}
        except Exception as e:
            logger.error(f"Error fetching weather for {city}: {str(e)}")
            return {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'city': city, 'temperature': None}

    def append_to_database(self, data: List[Dict]):
        """Append weather data to SQLite database."""
        try:
            with sqlite3.connect(self.database_file) as conn:
                cursor = conn.cursor()
                valid_data = [d for d in data if d['city'] and isinstance(d['city'], str)]
                if not valid_data:
                    logger.warning("No valid weather data to append")
                    return
                cursor.executemany(
                    "INSERT INTO weather_data (time, city, temperature) VALUES (?, ?, ?)",
                    [(d['time'], d['city'], d['temperature']) for d in valid_data]
                )
                conn.commit()
                logger.info(f"Appended {len(valid_data)} records to {self.database_file}")
        except sqlite3.Error as e:
            logger.error(f"Error appending to database: {str(e)}")