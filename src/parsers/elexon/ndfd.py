def ndfd_parser(record):
    return {
        "publish_time": record["publishTime"],
        "forecast_date": record["forecastDate"],
        "forecast_demand": record["demand"]
    }