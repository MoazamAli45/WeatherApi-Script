import re
from typing import List

# Configuration
API_KEY = "a5a004fba0c5464fa7a124259251306"  
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
EXCEL_FILE = "weather_data.xlsx"
INPUT_FILE = "cities.xlsx"
UPDATE_INTERVAL = 1  # minutes (change to 15 for production)

def validate_api_key(api_key: str) -> bool:
    """Validate API key format (basic check for non-empty and typical length)."""
    if not api_key or len(api_key) < 10 or not re.match(r'^[a-zA-Z0-9-]+$', api_key):
        return False
    return True