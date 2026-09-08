from datetime import datetime, timedelta, timezone
import pandas as pd

from src.utils.sessions import elexon_session
from src.data_sources.elexon.fuelhh import get_fuelhh
from src.parsers.elexon.fuelhh import fuelhh_parser

def get_live_generation(session):
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(hours = 12)

    start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    response = get_fuelhh(
        session = session,
        publish_date_time_from = start_date,
        publish_date_time_to = end_date
    )

    rows = [fuelhh_parser(record) for record in response]

    return pd.DataFrame(rows).drop(columns = "source")

if __name__ == "__main__":
    retry_session = elexon_session()
    
    response = get_live_generation(
        session = retry_session
    )

    print(response)