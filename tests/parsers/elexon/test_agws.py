from data.responses.agws_response import agws_response
from src.parsers.elexon.agws import agws_parser

def test_agws_parser():
    result = [agws_parser(record) for record in agws_response]

    assert result == [
        {
            "publish_time": "2026-08-23T18:30:04Z",
            "start_time": "2026-08-23T16:00:00Z",
            "fuel_type": "Wind Onshore",
            "generation": 508.0,
        },
        {
            "publish_time": "2026-08-23T18:30:04Z",
            "start_time": "2026-08-23T16:00:00Z",
            "fuel_type": "Wind Offshore",
            "generation": 798.0,
        },
        {
            "publish_time": "2026-08-23T18:30:04Z",
            "start_time": "2026-08-23T16:00:00Z",
            "fuel_type": "Solar",
            "generation": 5602.0,
        },
    ]