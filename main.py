import schedule
import time
import logging
import requests
from config import UPDATE_INTERVAL

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API_URL = "http://127.0.0.1:8000/weather"  # Local FastAPI server

#   DOCKERIZE API URL
API_URL = "http://weather-api:8000/weather" 
def update_weather():
    """Fetch weather data from FastAPI endpoint."""
    logger.info("Running update_weather job")
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            logger.info(f"Received weather data: {data['data']}")
        else:
            logger.warning("No weather data received")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")

def start():
    """Start the weather monitoring scheduler."""
    logger.info("Starting weather monitoring script")
    
    # Run immediately on start
    update_weather()
    
    # Schedule updates
    schedule.every(UPDATE_INTERVAL).minutes.do(update_weather)
    logger.info(f"Scheduled weather updates every {UPDATE_INTERVAL} minute(s)")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Script terminated by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    start()