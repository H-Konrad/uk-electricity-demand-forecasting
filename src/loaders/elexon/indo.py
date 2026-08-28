from datetime import datetime, timedelta

from src.utils.sessions import elexon_session
from src.data_sources.elexon.indo import get_indo
from src.parsers.elexon.indo import indo_parser
from src.database.insert_data import InsertToDatabase
from src.utils.sessions import elexon_session

def load_indo(start_date, end_date, db, hour_window, session):
    start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    end_date = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    while start_date < end_date:
        temp_end_date = min(start_date + timedelta(hours = hour_window - 0.5), end_date)

        response = get_indo(
            session = session,
            publish_date_time_from = start_date.isoformat().replace("+00:00", "Z"),
            publish_date_time_to = temp_end_date.isoformat().replace("+00:00", "Z")
        )

        rows = [indo_parser(record) for record in response]

        db.insert_demand(rows)

        print(f"Complete: {start_date} to {temp_end_date}")

        start_date = temp_end_date + timedelta(hours = 0.5)

if __name__ == "__main__":
    retry_session = elexon_session()
    
    #load_indo(
    #    start_date = "2026-07-01T00:30:00Z",
    #    end_date = "2026-08-01T00:00:00Z",
    #    db = InsertToDatabase(),
    #    hour_window = 14 * 24,
    #    session = retry_session()
    #)