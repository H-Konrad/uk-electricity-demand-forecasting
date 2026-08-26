import openmeteo_requests
import requests_cache
from retry_requests import retry

from src.parsers.open_meteo.uk_met_office import uk_met_office_parser

url = "https://single-runs-api.open-meteo.com/v1/forecast"

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
        run,
        hourly = [
            "temperature_2m", 
            "relative_humidity_2m", 
            "apparent_temperature",
            "snowfall",
            "rain",
            "showers",
            "weather_code"
        ],
        models = "ukmo_uk_deterministic_2km"
    ):
    openmeteo = openmeteo_requests.Client(
        session = retry_session
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly,
        "models": models,
        "forecast_days": 1,
        "run": run
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
    run = "2026-08-25T00:00"

    response = get_weather_data(
        latitude = latitude,
        longitude = longitude,
        run = run
    )

    a = uk_met_office_parser(
        run = run,
        response = response[0]
    )

    print(a)
