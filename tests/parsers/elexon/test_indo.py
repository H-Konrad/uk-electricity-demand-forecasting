from data.responses.indo_response import indo_response
from src.parsers.elexon.indo import indo_parser

def test_indo_parser():
    result = [indo_parser(record) for record in indo_response]

    assert result == [
        {
            "publish_time": "2026-08-23T19:00:00Z",
            "start_time": "2026-08-23T18:30:00Z",
            "true_demand": 26128,
        },
        {
            "publish_time": "2026-08-23T18:30:00Z",
            "start_time": "2026-08-23T18:00:00Z",
            "true_demand": 25852,
        },
        {
            "publish_time": "2026-08-23T18:00:00Z",
            "start_time": "2026-08-23T17:30:00Z",
            "true_demand": 25365,
        },
    ]