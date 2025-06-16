import schedule
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from weather_api import WeatherAPI
from config import UPDATE_INTERVAL, validate_api_key, API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeatherScheduler:
    """Class to handle weather data scheduling and updates."""
    
    def __init__(self, max_workers: int = 5):
        self.weather_api = WeatherAPI()
        self.max_workers = max_workers
    
    def update_weather(self):
        """Main function to update weather data for all cities using threads."""
        logger.info("Running update_weather job")
        cities = self.weather_api.read_cities()
        if not cities:
            logger.warning("No cities to process")
            return
        
        # Fetch weather data in parallel with max 5 threads
        logger.info(f"Fetching weather data for {len(cities)} cities with {min(self.max_workers, len(cities))} threads")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            weather_data = list(executor.map(self.weather_api.fetch_weather_data, cities))
        
        if weather_data:
            self.weather_api.append_to_database(weather_data)
            logger.info(f"Completed weather data fetch for {len(cities)} cities")

    def start(self):
        """Start the weather monitoring scheduler."""
        logger.info("Starting weather monitoring script")
        
        if not validate_api_key(API_KEY):
            logger.error("Script cannot start due to invalid API key")
            return
        
        # Run immediately on start
        self.update_weather()
        
        # Schedule updates
        schedule.every(UPDATE_INTERVAL).minutes.do(self.update_weather)
        logger.info(f"Scheduled weather updates every {UPDATE_INTERVAL} minute(s)")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)  # Reduced sleep for better scheduling accuracy
        except KeyboardInterrupt:
            logger.info("Script terminated by user")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    scheduler = WeatherScheduler(max_workers=5)
    scheduler.start()