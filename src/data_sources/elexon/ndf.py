import requests
import requests_cache
from retry_requests import retry

elexon_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/NDF"

def get_ndf(
        session,
        publish_date_time_from, 
        publish_date_time_to
    ):
    params = {
        "publishDateTimeFrom": publish_date_time_from,
        "publishDateTimeTo": publish_date_time_to,
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

    start = "2026-08-23T18:00:00Z"
    end = "2026-08-23T18:30:00Z"

    data = get_ndf(
        session = retry_session,
        publish_date_time_from = start,
        publish_date_time_to = end
    )

    print(data)