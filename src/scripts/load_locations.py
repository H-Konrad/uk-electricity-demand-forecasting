from src.database.insert_data import InsertToDatabase
from data_sources.open_meteo.locations import locations

def main():
    db = InsertToDatabase()

    try:
        db.insert_locations(locations)
    finally:
        db.close()

if __name__ == "__main__":
    main()