import sqlite3
import logging
import os
from typing import List, Dict
from datetime import datetime
from config import DATABASE_FILE

# Configure logging
logger = logging.getLogger(__name__)

class Database:
    """Class to manage SQLite database connections and operations."""
    
    def __init__(self):
        self.database_file = DATABASE_FILE
    
    def get_connection(self):
        """Establish a connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.database_file)
            logger.info(f"Connected to database: {os.path.abspath(self.database_file)}")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {str(e)}")
            raise
    
    def init_tables(self):
        """Initialize database tables if they don't exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cities (
                        city TEXT NOT NULL UNIQUE
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS weather_data (
                        time TIMESTAMP NOT NULL,
                        city TEXT NOT NULL,
                        temperature REAL
                    )
                """)
                conn.commit()
                logger.info(f"Initialized tables in {self.database_file}")
        except sqlite3.Error as e:
            logger.error(f"Error initializing tables: {str(e)}")
            raise
    
    def read_cities(self) -> List[str]:
        """Read city names from cities table."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cities'")
                if not cursor.fetchone():
                    logger.error("Cities table does not exist")
                    return []
                cursor.execute("SELECT city FROM cities WHERE city IS NOT NULL AND city != ''")
                cities = [row[0] for row in cursor.fetchall()]
                logger.info(f"Read {len(cities)} cities from {self.database_file}")
                return cities
        except sqlite3.Error as e:
            logger.error(f"Error reading cities: {str(e)}")
            return []
    
    def add_cities(self, cities: List[str]):
        """Add cities to the cities table, ignoring duplicates."""
        try:
            with self.get_connection() as conn:
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
    
    def append_weather_data(self, data: List[Dict]):
        """Append weather data to SQLite database."""
        try:
            with self.get_connection() as conn:
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