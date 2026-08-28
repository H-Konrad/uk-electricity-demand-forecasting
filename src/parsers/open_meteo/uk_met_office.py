import pandas as pd

def uk_met_office_parser(
        location_id,
        response
    ):
    hourly = response.Hourly()

    hourly_data = {
        "date": pd.date_range(
            start = pd.to_datetime(
                hourly.Time(), 
                unit = "s", 
                utc = True
            ),
            end = pd.to_datetime(
                hourly.TimeEnd(), 
                unit = "s", 
                utc = True
            ),
            freq = pd.Timedelta(
                seconds = hourly.Interval()
            ),
            inclusive = "left"
        )
    }

    return pd.DataFrame({
        "location_id": location_id,
        "forecast_time": hourly_data["date"],
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy().round(2),
        "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy().round(2),
        "apparent_temperature": hourly.Variables(2).ValuesAsNumpy().round(2),
        "snowfall": hourly.Variables(3).ValuesAsNumpy().round(2),
        "rain": hourly.Variables(4).ValuesAsNumpy().round(2)
    })