import requests

from src.utils.sessions import elexon_session

elexon_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/NDFD"

def get_ndfd(
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
    retry_session = elexon_session()

    start = "2026-08-23T18:00:00Z"
    end = "2026-08-24T18:00:00Z"

    data = get_ndfd(
        session = retry_session,
        publish_date_time_from = start,
        publish_date_time_to = end
    )

    print(data)