import pandas as pd
from datetime import date, timedelta

from src.data_sources.open_meteo.uk_met_office_forecast import get_weather_forecast_data
from src.parsers.open_meteo.uk_met_office import uk_met_office_parser
from src.data_sources.open_meteo.locations import locations

def get_live_weather_data(latitude, longitude, session):
    location_names = pd.DataFrame(locations).drop(columns = [
        "latitude",
        "longitude"
    ])

    current_date = date.today()
    start_date = current_date - timedelta(days = 1)
    end_date = current_date + timedelta(days = 1)

    response = get_weather_forecast_data(
        session = session,
        latitude = latitude,
        longitude = longitude,
        start_date = start_date,
        end_date = end_date
    )

    rows = []
    for i in range(len(latitude)):
        location_df = uk_met_office_parser(
            location_id = i + 1,
            response = response[i]
        )

        rows.append(location_df)

    rows = pd.concat(rows, ignore_index = True)

    rows = rows.merge(
        location_names,
        on = "location_id"
    )

    rows["forecast_time"] = rows["forecast_time"].astype("datetime64[us, UTC]")

    return rows.drop(columns = "location_id")