import requests

elexon_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/AGWS"

def get_agws(
        session,
        publish_date_time_from = None, 
        publish_date_time_to = None
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

        return response.json()["data"]

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None