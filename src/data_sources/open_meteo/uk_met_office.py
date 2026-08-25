import openmeteo_requests
import requests_cache
from retry_requests import retry

url = "https://api.open-meteo.com/v1/forecast"

cache_session = requests_cache.CachedSession(
    cache_name = '.weather_cache', 
    expire_after = 3600
)
retry_session = retry(
    cache_session, 
    retries = 5, 
    backoff_factor = 0.2
)

def get_weather_data(
        latitude, 
        longitude,
        start_date,
        end_date,
        hourly = [
            "temperature_2m", 
            "relative_humidity_2m", 
            "apparent_temperature",
            "snowfall",
            "rain",
            "showers",
            "weather_code"
        ],
        models = "ukmo_seamless"
    ):
    openmeteo = openmeteo_requests.Client(
        session = retry_session
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly,
        "models": models,
        "start_date": start_date,
        "end_date": end_date,
    }

    try:
        response = openmeteo.weather_api(
            url = url, 
            params = params
        )

        return response

    except Exception as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    latitude = 51.5085
    longitude = -0.1257
    start_date = "2026-08-18"
    end_date = "2026-08-19"

    response = get_weather_data(
        latitude = latitude,
        longitude = longitude,
        start_date = start_date,
        end_date = end_date
    )

