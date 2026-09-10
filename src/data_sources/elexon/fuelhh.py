import requests

elexon_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"

def get_fuelhh(
        session,
        settlement_date_from = None,
        settlement_date_to = None,
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