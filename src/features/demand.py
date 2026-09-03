import pandas as pd

def fill_demand_gaps(demand):
    demand = demand.sort_values("start_time").set_index("start_time")

    timeline = pd.date_range(
        start = demand.index.min(),
        end = demand.index.max(),
        freq = "30min",
        tz = demand.index.tz
    )

    demand = demand.reindex(timeline)
    demand["true_demand_mw"] = demand["true_demand_mw"].interpolate(
        method = "linear", 
        limit = 4, 
        limit_area = "inside"
    )

    demand = demand.rename_axis("start_time").reset_index()

    demand = demand.rename(columns = {
        "start_time": "prediction_time"
    })

    return demand

def half_day_lags(demand):
    demand = demand.copy()

    demand["demand_lag_30m"] = demand["true_demand_mw"].shift(1)
    demand["demand_lag_1h"] = demand["true_demand_mw"].shift(2)
    demand["demand_lag_2h"] = demand["true_demand_mw"].shift(4)
    demand["demand_lag_6h"] = demand["true_demand_mw"].shift(12)
    demand["demand_lag_12h"] = demand["true_demand_mw"].shift(24)

    demand["demand_rolling_3h"] = demand["true_demand_mw"].shift(1).rolling(6).mean().round(0)
    demand["demand_rolling_6h"] = demand["true_demand_mw"].shift(1).rolling(12).mean().round(0)
    demand["demand_rolling_12h"] = demand["true_demand_mw"].shift(1).rolling(24).mean().round(0)

    return demand