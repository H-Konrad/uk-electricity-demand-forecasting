from datetime import datetime, timedelta

from src.utils.sessions import elexon_session
from src.data_sources.elexon.ndfd import get_ndfd
from src.parsers.elexon.ndfd import ndfd_parser
from src.database.insert_data import InsertToDatabase
from src.utils.sessions import elexon_session

def load_ndfd(start_date, end_date, db, session):
    start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    end_date = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    while start_date < end_date:
        temp_end_date = min(start_date + timedelta(days = 1), end_date)

        response = get_ndfd(
            session = session,
            publish_date_time_from = start_date.isoformat().replace("+00:00", "Z"),
            publish_date_time_to = temp_end_date.isoformat().replace("+00:00", "Z")
        )

        rows = [ndfd_parser(record) for record in response]

        db.insert_ndfd(rows)

        print(f"Complete: {start_date} to {temp_end_date}")

        start_date = temp_end_date

if __name__ == "__main__":
    retry_session = elexon_session()
    
    #load_ndfd(
    #    start_date = "2026-07-01T00:00:00Z",
    #    end_date = "2026-07-03T00:00:00Z",
    #    db = InsertToDatabase(),
    #    session = retry_session()
    #)