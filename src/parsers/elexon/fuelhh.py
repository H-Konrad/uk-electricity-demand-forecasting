def fuelhh_parser(record):
    return {
        "source": "FUELHH",
        "publish_time": record["publishTime"],
        "start_time": record["startTime"],
        "fuel_type": record["fuelType"],
        "generation_mw": record["generation"]
    }