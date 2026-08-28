from datetime import datetime, timedelta
import pandas as pd

from src.utils.sessions import weather_data_session
from src.data_sources.open_meteo.uk_met_office import get_weather_data
from src.parsers.open_meteo.uk_met_office import uk_met_office_parser
from src.database.insert_data import InsertToDatabase

def load_weather_data(start_date, end_date, latitude, longitude, db, day_window, session):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while start_date < end_date:
        temp_end_date = min(start_date + timedelta(days = day_window - 1), end_date)

        response = get_weather_data(
            session = session,
            latitude = latitude,
            longitude = longitude,
            start_date = start_date.date(),
            end_date = temp_end_date.date()
        )

        rows = []
        for i in range(len(latitude)):
            location_df = uk_met_office_parser(
                location_id = i + 1,
                response = response[i]
            )

            rows.append(location_df)

        rows = pd.concat(rows, ignore_index = True)
        db.insert_weather(rows.to_dict("records"))

        print(f"Complete: {start_date} to {temp_end_date}")

        start_date = temp_end_date + timedelta(days = 1)

if __name__ == "__main__":
    session = weather_data_session()
    
    #load_weather_data(
    #    start_date = "2026-08-10",
    #    end_date = "2026-08-12",
    #    latitude = [57.4777, 55.9532],
    #    longitude = [-4.2247, -3.1883],
    #    db = InsertToDatabase(),
    #    day_window = 7,
    #    session = session
    #)