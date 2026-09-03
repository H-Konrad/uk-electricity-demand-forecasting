import pandas as pd

def create_horizon_dataset(demand):
    horizon_dfs = []

    for horizon in range(48):
        df = demand.copy()
        df["horizon"] = horizon + 1 
        df["target_time"] = df["prediction_time"] + pd.Timedelta(minutes = 30 * (horizon))

        horizon_dfs.append(df)

    modelling = pd.concat(
        objs = horizon_dfs,
        ignore_index = True
    )

    target_demand = demand[["prediction_time", "true_demand_mw"]].rename(columns = {
        "true_demand_mw": "target_demand"
    })

    modelling = modelling.merge(
        right = target_demand,
        left_on = "target_time",
        right_on = "prediction_time",
        how = "left"
    )

    modelling = modelling.drop(columns = [
        "true_demand_mw",
        "prediction_time_y"
    ]).rename(columns = {
        "prediction_time_x": "reference_time"
    })

    return modelling

def add_dynamic_demand_lags(modelling, demand):
    demand_basic = demand[["prediction_time", "true_demand_mw"]].copy()

    lag_times = {
        "24h": pd.Timedelta(hours = 24),
        "48h": pd.Timedelta(hours = 48),
        "7d": pd.Timedelta(days = 7)
    }

    for label, time in lag_times.items():
        lookup = demand_basic.rename(columns = {
            "prediction_time": "lag_time",
            "true_demand_mw": f"demand_lag_{label}"
        })

        modelling["lag_time"] = modelling["target_time"] - time

        modelling = modelling.merge(
            right = lookup,
            on = "lag_time",
            how = "left"
        ).drop(columns = "lag_time")

    modelling = modelling.sort_values(["reference_time", "horizon"]).dropna().reset_index(drop = True)

    return modelling