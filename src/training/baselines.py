def get_baseline_predictions(dataset):
    df = dataset.copy()

    df["baseline_30m"] = df["demand_lag_30m"]
    df["baseline_24h"] = df["demand_lag_24h"]
    df["baseline_7d"] = df["demand_lag_7d"]

    return df[[
        "reference_time", 
        "target_time",
        "target_demand",
        "horizon",
        "baseline_30m",
        "baseline_24h",
        "baseline_7d"
    ]]