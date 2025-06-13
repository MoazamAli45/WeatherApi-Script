# Weather Monitoring System

This Python project fetches current weather data (temperature) for a list of cities from the WeatherAPI and saves it to an Excel file. It runs on a schedule to update the data at regular intervals.

## Features

* Reads city names from an Excel file (`cities.xlsx`).
* Fetches temperature data for each city using the WeatherAPI.
* Saves the time, city, and temperature to an output Excel file (`weather_data.xlsx`).
* Runs on a configurable schedule (e.g., every 1 minute for testing, 15 minutes for production).
* Uses environment variables for secure API key storage.
* Modular design with separate configuration, API handling, and scheduling logic.

## Project Structure

├── config.py           # Configuration and API key validation
├── weather_api.py      # WeatherAPI interaction and data storage
├── main.py             # Scheduling and main program logic
├── cities.xlsx         # Input Excel file with city names
├── .env                # Environment variables (API key)
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation


## Prerequisites

* Python 3.8 or higher
* A WeatherAPI account and API key (sign up at [WeatherAPI](https://www.weatherapi.com/))
* Required Python libraries: `requests`, `pandas`, `schedule`, `python-dotenv`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/MoazamAli45/WeatherApi-Script.git](https://github.com/MoazamAli45/WeatherApi-Script)
    cd your-repo-name
    ```

2.  **Set up a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install requests pandas schedule python-dotenv
    ```

4.  **Create a `.env` file** in the project root with your WeatherAPI key:
    ```
    WEATHER_API_KEY=your_api_key_here
    ```

5.  **Prepare the input file:**
    * Create an Excel file named `cities.xlsx`.
    * Add a single column named `City` with the names of the cities you want to monitor.

    **Example `cities.xlsx`:**
    | City   |
    |--------|
    | London |
    | Paris  |
    | Tokyo  |

## Usage

Run the main script from your terminal:

```bash
python main.py
The script will:

Read the list of cities from cities.xlsx.
Fetch the current weather data for each city.
Save the results to weather_data.xlsx.
Repeat the process based on the UPDATE_INTERVAL in config.py.
To stop the script, press Ctrl+C.

Configuration
You can customize the script's behavior by editing the config.py file:

UPDATE_INTERVAL: Set the time between updates (in minutes). The default is 1 for testing.
WEATHER_API_URL: The API endpoint.
EXCEL_FILE: The name of the output file (default: weather_data.xlsx).
INPUT_FILE: The name of the input city file (default: cities.xlsx).
Notes
Security: The .gitignore file is configured to prevent the .env file and weather_data.xlsx from being committed to version control. Do not share your API key publicly.
Error Handling: The script includes basic error handling and will log issues like an invalid API key or a missing file to the console.
Production Use: For production, it is recommended to set the UPDATE_INTERVAL to 15 minutes or higher to stay within the free tier limits of the WeatherAPI.