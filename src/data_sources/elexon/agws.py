import requests

elexon_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/AGWS"

def get_agws(
        publish_date_time_from = None, 
        publish_date_time_to = None
    ):
    try:
        params = {
            "publishDateTimeFrom": publish_date_time_from,
            "publishDateTimeTo": publish_date_time_to,
            "format": "json"
        }

        response = requests.get(
            url = elexon_url,
            params = params,
            headers = {
                "Cache-Control": "no-cache"
            },
            timeout = 30
        )

        response.raise_for_status()

        data = response.json()

        return data["data"]

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    start = "2026-08-23T18:00:00Z"
    end = "2026-08-23T19:00:00Z"

    data = get_agws(
        publish_date_time_from = start,
        publish_date_time_to = end
    )

    print(data)