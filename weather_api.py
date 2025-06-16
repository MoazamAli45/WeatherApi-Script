import requests
import pandas as pd
import logging
from typing import List, Dict
from datetime import datetime
import os
from config import API_KEY, WEATHER_API_URL, EXCEL_FILE, INPUT_FILE, validate_api_key

# Configure logging (only once, controlled by main.py)
logger = logging.getLogger(__name__)

class WeatherAPI:
    """Class to handle weather API interactions and data storage."""
    
    def __init__(self, timeout: int = 10):
        self.api_key = API_KEY
        self.api_url = WEATHER_API_URL
        self.excel_file = EXCEL_FILE
        self.input_file = INPUT_FILE
        self.timeout = timeout
        
        if not validate_api_key(self.api_key):
            logger.error("Invalid API key provided")
            raise ValueError("Invalid API key")
    
    def read_cities(self) -> List[str]:
        """Read city names from Excel file under 'City' column."""
        try:
            df = pd.read_excel(self.input_file)
            if 'City' not in df.columns:
                logger.error(f"'City' column not found in {self.input_file}")
                return []
            cities = df['City'].dropna().str.strip().tolist()
            logger.info(f"Read {len(cities)} cities from {self.input_file}")
            return cities
        except FileNotFoundError:
            logger.error(f"Input file {self.input_file} not found")
            return []
        except Exception as e:
            logger.error(f"Error reading cities: {str(e)}")
            return []

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

    def append_to_excel(self, data: List[Dict]):
        """Append weather data to Excel file with Time, City, Temperature columns."""
        try:
            df_new = pd.DataFrame(data, columns=['time', 'city', 'temperature'])
            df_new = df_new.dropna(subset=['city'])
            if os.path.exists(self.excel_file):
                df_existing = pd.read_excel(self.excel_file)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_combined = df_new
            
            df_combined.to_excel(self.excel_file, index=False, columns=['time', 'city', 'temperature'])
            logger.info(f"Appended {len(df_new)} records to {self.excel_file}")
        except Exception as e:
            logger.error(f"Error appending to Excel: {str(e)}")