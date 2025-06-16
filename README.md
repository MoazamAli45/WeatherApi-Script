# Weather Monitoring Application

## Overview
This project is a weather monitoring application built with **FastAPI** that fetches real-time weather data from the WeatherAPI for a list of cities stored in a SQLite database. The application includes a client script that periodically retrieves weather data via a RESTful API endpoint. The data is stored in a `weather.db` database for persistence and analysis.

- **API**: FastAPI server running at `http://127.0.0.1:8000`.
- **Database**: SQLite (`weather.db`) with `cities` and `weather_data` tables.
- **Default Cities**: Pre-populated with 5 major cities in Pakistan (Islamabad, Karachi, Lahore, Rawalpindi, Faisalabad).
- **Client**: A Python script that schedules weather updates every 15 minutes.

## Features
- Fetch and store weather data for configured cities.
- RESTful API endpoint (`/weather`) to retrieve and update weather data.
- Automatic initialization of the database with default cities.
- Logging for debugging and monitoring.
- Support for adding or modifying cities via the database.

## Prerequisites
- Python 3.8 or higher.
- Internet connection for WeatherAPI requests.
- An API key from [WeatherAPI](https://www.weatherapi.com/).

