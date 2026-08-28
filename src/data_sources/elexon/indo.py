import requests

from src.utils.sessions import elexon_session

elexon_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/INDO"

def get_indo(
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

    start = "2026-07-18T00:30:00Z"
    end = "2026-07-19T00:00:00Z"

    data = get_indo(
        session = retry_session,
        publish_date_time_from = start,
        publish_date_time_to = end
    )

    print(data)