def agws_parser(record):
    return {
        "publish_time": record["publishTime"],
        "start_time": record["startTime"],
        "fuel_type": record["psrType"],
        "generation": record["quantity"]
    }