from src.database.insert_data import InsertToDatabase
from src.utils.sessions import weather_data_session
from src.data_sources.open_meteo.locations import locations
from src.loaders.open_meteo.uk_met_office import load_weather_data

def get_lat_lon():
    latitude = []
    longitude = []
    for location in locations:
        latitude.append(location["latitude"])
        longitude.append(location["longitude"])

    return latitude, longitude

def main():
    session = weather_data_session()
    db = InsertToDatabase()
    latitude, longitude = get_lat_lon()

    try:
        print("########## UK Met Office ##########")
        load_weather_data(
            start_date = "2023-08-01",
            end_date = "2026-08-01",
            latitude = latitude,
            longitude = longitude,
            db = db,
            day_window = 30,
            session = session
        )

    finally:
        db.close()

if __name__ == "__main__":
    main()