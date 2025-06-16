import re
from dotenv import load_dotenv
import os

# Load environment variables from .env file
if not load_dotenv():
    raise ValueError("Failed to load .env file. Ensure it exists and is readable.")

# Configuration
API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise ValueError("WEATHER_API_KEY not found in environment variables")

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
DATABASE_FILE = "weather.db"  # Updated to match the file you're using in DB4S
UPDATE_INTERVAL = 1  # minutes (change to 15 for production)

def validate_api_key(api_key: str) -> bool:
    """Validate API key format."""
    if not api_key or len(api_key) < 10 or not re.match(r'^[a-zA-Z0-9-]+$', api_key):
        return False
    return True