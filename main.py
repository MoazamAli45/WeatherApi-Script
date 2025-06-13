import schedule
import time
import logging
from weather_api import WeatherAPI
from config import UPDATE_INTERVAL, validate_api_key, API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeatherScheduler:
    """Class to handle weather data scheduling and updates."""
    
    def __init__(self):
        self.weather_api = WeatherAPI()
    
    def update_weather(self):
        """Main function to update weather data for all cities."""
        logger.info("Running update_weather job")
        cities = self.weather_api.read_cities()
        if not cities:
            logger.warning("No cities to process")
            return
        
        weather_data = []
        for city in cities:
            weather_data.append(self.weather_api.fetch_weather_data(city))
        
        if weather_data:
            self.weather_api.append_to_excel(weather_data)

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
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("Script terminated by user")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    scheduler = WeatherScheduler()
    scheduler.start()