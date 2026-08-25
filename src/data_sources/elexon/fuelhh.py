import requests
import requests_cache
from retry_requests import retry

elexon_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"

def get_fuelhh(
        session,
        settlement_date_from,
        settlement_date_to,
        publish_date_time_from = None, 
        publish_date_time_to = None,
        settlement_period = None,
        fuel_type = None
    ):
    params = {
        "publishDateTimeFrom": publish_date_time_from,
        "publishDateTimeTo": publish_date_time_to,
        "settlementDateFrom": settlement_date_from,
        "settlementDateTo": settlement_date_to,
        "settlementPeriod": settlement_period,
        "fuelType": fuel_type,
        "format": "json"
    }

    try:
        response = session.get(
            url = elexon_url,
            params = params,
            timeout = 30
        )

        response.raise_for_status()

        data = response.json()

        return data["data"]

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    cache_session = requests_cache.CachedSession(
        cache_name = '.elexon_cache', 
        expire_after = 3600
    )
    retry_session = retry(
        cache_session, 
        retries = 5, 
        backoff_factor = 0.2
    )

    start = "2026-08-23"
    end = "2026-08-23"
    settlement_period = 1

    data = get_fuelhh(
        session = retry_session,
        settlement_date_from = start,
        settlement_date_to = end,
        settlement_period = settlement_period
    )

    print(data)