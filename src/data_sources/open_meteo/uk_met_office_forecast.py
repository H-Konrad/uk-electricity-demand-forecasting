import openmeteo_requests

from src.parsers.open_meteo.uk_met_office_forecast import uk_met_office_forecast_parser
from src.utils.sessions import weather_data_session

url = "https://api.open-meteo.com/v1/forecast"

def get_weather_data(
        session,
        latitude, 
        longitude,
        start_date,
        end_date,
        hourly = [
            "temperature_2m", 
            "relative_humidity_2m", 
            "snowfall",
            "rain",
        ],
        models = "ukmo_uk_deterministic_2km"
    ):
    openmeteo = openmeteo_requests.Client(
        session = session
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
    retry_session = weather_data_session()

    latitude = [51.5085, 55.9532]
    longitude = [-0.1257, -3.1883]
    start_date = "2026-09-08",
    end_date = "2026-09-09"

    response = get_weather_data(
        session = retry_session,
        latitude = latitude,
        longitude = longitude,
        start_date = start_date,
        end_date = end_date
    )

    print(response)
 
    loc_a = uk_met_office_forecast_parser(
        location_id = 0, 
        response = response[0]
    )

    print(loc_a)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")

    loc_b = uk_met_office_forecast_parser(
        location_id = 1,
        response = response[1]
    )

    print(loc_b)
