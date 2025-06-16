import requests
import logging
import time
from fastapi import FastAPI, HTTPException
from asyncio import gather
from database import Database
from config import API_KEY, WEATHER_API_URL, validate_api_key
from datetime import datetime
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
db = Database()
db.init_tables()

if not validate_api_key(API_KEY): # type: ignore
    logger.error("Invalid API key provided")
    raise ValueError("Invalid API key")

def fetch_weather_data(city: str) -> Dict:
    """Fetch weather data for a single city from WeatherAPI with a simulated delay."""
    params = {'key': API_KEY, 'q': city, 'aqi': 'no'}
    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'error' in data:
            logger.error(f"API error for {city}: {data['error']['message']}")
            raise HTTPException(status_code=400, detail=data['error']['message'])
        # Simulate a 2-second delay
        time.sleep(2)
        weather_info = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'city': city,
            'temperature': data['current']['temp_c']
        }
        logger.info(f"Fetched weather for {city}: {weather_info['temperature']}°C")
        return weather_info
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            logger.error(f"Unauthorized API key for {city}")
            raise HTTPException(status_code=401, detail="Invalid API key")
        elif e.response.status_code == 400:
            logger.error(f"Invalid city name or query for {city}")
            raise HTTPException(status_code=400, detail="Invalid city name")
        else:
            logger.error(f"HTTP error fetching weather for {city}: {str(e)}")
            raise HTTPException(status_code=500, detail="Server error")
    except Exception as e:
        logger.error(f"Error fetching weather for {city}: {str(e)}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/weather")
async def get_weather():
    """Fetch and store weather data for all cities."""
    cities = db.read_cities()
    if not cities:
        logger.warning("No cities to process")
        raise HTTPException(status_code=404, detail="No cities configured")
    
    weather_data = []
    for city in cities:
        try:
            weather = fetch_weather_data(city)
            weather_data.append(weather)
        except HTTPException as e:
            logger.warning(f"Skipped {city} due to error: {str(e.detail)}")
            weather_data.append({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'city': city, 'temperature': None})
    
    db.append_weather_data(weather_data)
    return {"status": "success", "data": weather_data}