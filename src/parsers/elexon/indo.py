def indo_parser(record):
    return {
        "publish_time": record["publishTime"],
        "start_time": record["startTime"],
        "true_demand": record["demand"]
    }