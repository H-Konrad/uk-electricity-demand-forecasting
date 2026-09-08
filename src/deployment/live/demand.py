from datetime import datetime, timedelta, timezone
import pandas as pd

from src.utils.sessions import elexon_session
from src.data_sources.elexon.indo import get_indo
from src.parsers.elexon.indo import indo_parser

def get_live_demand(session):
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days = 8)

    start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    response = get_indo(
        session = session,
        publish_date_time_from = start_date,
        publish_date_time_to = end_date
    )

    rows = [indo_parser(record) for record in response]

    return pd.DataFrame(rows).drop(
        columns = "publish_time"
    ).sort_values("start_time").reset_index(drop = True)

if __name__ == "__main__":
    retry_session = elexon_session()
    
    response = get_live_demand(
        session = retry_session
    )

    print(response)

