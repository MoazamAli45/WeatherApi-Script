import requests
import logging
from concurrent.futures import ThreadPoolExecutor
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = "http://127.0.0.1:8000/weather"
NUM_REQUESTS = 5 # Number of concurrent requests

def make_request():
    """Make a single request to the weather endpoint."""
    start_time = time.time()
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        elapsed_time = time.time() - start_time
        logger.info(f"Request completed in {elapsed_time:.2f} seconds: {data['status']}")
    except requests.exceptions.RequestException as e:
        elapsed_time = time.time() - start_time
        logger.error(f"Request failed in {elapsed_time:.2f} seconds: {str(e)}")

def run_test():
    """Run multiple concurrent requests."""
    logger.info(f"Starting test with {NUM_REQUESTS} concurrent requests")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
        executor.map(make_request, range(NUM_REQUESTS))
    
    total_time = time.time() - start_time
    logger.info(f"Test completed in {total_time:.2f} seconds")

if __name__ == "__main__":
    run_test()