def agws_parser(record):
    return {
        "source": "AGWS",
        "publish_time": record["publishTime"],
        "start_time": record["startTime"],
        "fuel_type": record["psrType"],
        "generation_mw": record["quantity"]
    }