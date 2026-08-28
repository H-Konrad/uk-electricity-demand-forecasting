from data.responses.fuelhh_response import fuelhh_response
from src.parsers.elexon.fuelhh import fuelhh_parser

def test_fuelhh_parser():
    result = [fuelhh_parser(record) for record in fuelhh_response]

    assert result == [
        {
            "source": "FUELHH",
            "publish_time": "2026-08-22T23:30:00Z",
            "start_time": "2026-08-22T23:00:00Z",
            "fuel_type": "BIOMASS",
            "generation": 3222,
        },
        {
            "source": "FUELHH",
            "publish_time": "2026-08-22T23:30:00Z",
            "start_time": "2026-08-22T23:00:00Z",
            "fuel_type": "CCGT",
            "generation": 3475,
        },
        {
            "source": "FUELHH",
            "publish_time": "2026-08-22T23:30:00Z",
            "start_time": "2026-08-22T23:00:00Z",
            "fuel_type": "COAL",
            "generation": 0,
        },
        {
            "source": "FUELHH",
            "publish_time": "2026-08-22T23:30:00Z",
            "start_time": "2026-08-22T23:00:00Z",
            "fuel_type": "INTELEC",
            "generation": 996,
        },
        {
            "source": "FUELHH",
            "publish_time": "2026-08-22T23:30:00Z",
            "start_time": "2026-08-22T23:00:00Z",
            "fuel_type": "INTEW",
            "generation": -532,
        },
    ]