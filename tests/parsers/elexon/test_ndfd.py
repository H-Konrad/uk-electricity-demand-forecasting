from data.responses.ndfd_response import ndfd_response
from src.parsers.elexon.ndfd import ndfd_parser

def test_ndfd_parser():
    result = [ndfd_parser(record) for record in ndfd_response]

    assert result == [
        {
            "publish_time": "2026-08-24T13:45:00Z",
            "forecast_date": "2026-08-26",
            "forecast_demand_mw": 28990,
        },
        {
            "publish_time": "2026-08-24T13:45:00Z",
            "forecast_date": "2026-08-27",
            "forecast_demand_mw": 29040,
        },
        {
            "publish_time": "2026-08-24T13:45:00Z",
            "forecast_date": "2026-08-28",
            "forecast_demand_mw": 26240,
        },
        {
            "publish_time": "2026-08-24T13:45:00Z",
            "forecast_date": "2026-08-29",
            "forecast_demand_mw": 23620,
        },
    ]