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
