import requests

elexon_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"

def get_fuelhh(
        settlement_date_from,
        settlement_date_to,
        publish_date_time_from = None, 
        publish_date_time_to = None,
        settlement_period = None,
        fuel_type = None
    ):
    try:
        params = {
            "publishDateTimeFrom": publish_date_time_from,
            "publishDateTimeTo": publish_date_time_to,
            "settlementDateFrom": settlement_date_from,
            "settlementDateTo": settlement_date_to,
            "settlementPeriod": settlement_period,
            "fuelType": fuel_type,
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
    start = "2026-08-23"
    end = "2026-08-23"
    settlement_period = 1

    data = get_fuelhh(
        settlement_date_from = start,
        settlement_date_to = end,
        settlement_period = settlement_period
    )

    print(data)