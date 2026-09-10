import openmeteo_requests

url = "https://api.open-meteo.com/v1/forecast"

def get_weather_forecast_data(
        session,
        latitude, 
        longitude,
        start_date,
        end_date,
        hourly = [
            "temperature_2m", 
            "apparent_temperature",
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