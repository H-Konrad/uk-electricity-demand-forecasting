import pandas as pd
from datetime import date, timedelta

from src.utils.sessions import weather_data_session
from src.data_sources.open_meteo.uk_met_office_forecast import get_weather_forecast_data
from src.parsers.open_meteo.uk_met_office_forecast import uk_met_office_forecast_parser
from src.data_sources.open_meteo.locations import locations

def get_live_weather_data(start_date, end_date, latitude, longitude, session):
    location_names = pd.DataFrame(locations).drop(columns = [
        "latitude",
        "longitude"
    ])

    response = get_weather_forecast_data(
        session = session,
        latitude = latitude,
        longitude = longitude,
        start_date = start_date,
        end_date = end_date
    )

    rows = []
    for i in range(len(latitude)):
        location_df = uk_met_office_forecast_parser(
            location_id = i + 1,
            response = response[i]
        )

        rows.append(location_df)

    rows = pd.concat(rows, ignore_index = True)

    rows = rows.merge(
        location_names,
        on = "location_id"
    )

    return rows.drop(columns = "location_id")


if __name__ == "__main__":
    session = weather_data_session()

    start_date = date.today()
    end_date = start_date + timedelta(days = 1)
    
    response = get_live_weather_data(
        start_date = start_date,
        end_date = end_date,
        latitude = [57.4777, 55.9532],
        longitude = [-4.2247, -3.1883],
        session = session
    )

    print(response)