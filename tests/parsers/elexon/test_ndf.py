from data.responses.ndf_response import ndf_response
from src.parsers.elexon.ndf import ndf_parser

def test_ndf_parser():
    result = [ndf_parser(record) for record in ndf_response]

    assert result == [
        {
            "publish_time": "2026-08-23T18:17:00Z",
            "forecast_time": "2026-08-23T18:30:00Z",
            "forecast_demand_mw": 25900,
        },
        {
            "publish_time": "2026-08-23T18:17:00Z",
            "forecast_time": "2026-08-23T19:00:00Z",
            "forecast_demand_mw": 25862,
        },
        {
            "publish_time": "2026-08-23T18:17:00Z",
            "forecast_time": "2026-08-23T19:30:00Z",
            "forecast_demand_mw": 25452,
        },
    ]