import openmeteo_requests
import requests_cache
from retry_requests import retry

from src.parsers.open_meteo.uk_met_office import uk_met_office_parser
from src.utils.sessions import weather_data_session

url = "https://historical-forecast-api.open-meteo.com/v1/forecast"

retry_session = weather_data_session()

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
        "start_date": start_date,
        "end_date": end_date
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
    latitude = [51.5085, 55.9532]
    longitude = [-0.1257, -3.1883]
    start_date = "2026-08-10"
    end_date = "2026-08-10"

    response = get_weather_data(
        latitude = latitude,
        longitude = longitude,
        start_date = start_date,
        end_date = end_date
    )

    a = uk_met_office_parser(
        response = response[0]
    )

    print(a)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")

    b = uk_met_office_parser(
        response = response[1]
    )

    print(b)
