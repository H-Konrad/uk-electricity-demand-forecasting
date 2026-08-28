def ndf_parser(record):
    return {
        "publish_time": record["publishTime"],
        "forecast_time": record["startTime"],
        "forecast_demand_mw": record["demand"]
    }