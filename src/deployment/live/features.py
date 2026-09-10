import pandas as pd

from src.deployment.live.demand import get_live_demand
from src.deployment.live.generation import get_live_generation
from src.deployment.live.weather import get_live_weather_data

from src.features.demand import fill_demand_gaps, half_day_lags
from src.features.generation import fill_generation_gaps, add_generation_features, pivot_generation
from src.features.weather import add_weather_features, pivot_weather
from src.features.modelling import (
    create_horizon_dataset, add_dynamic_demand_lags, merge_with_modelling, add_time_features
)
from src.data_sources.open_meteo.locations import locations

latitude = [location["latitude"] for location in locations]
longitude = [location["longitude"] for location in locations]

required_fuels = {
    "BIOMASS",
    "WIND",
    "PS",
    "OTHER",
    "OCGT",
    "NPSHYD",
    "NUCLEAR",
    "COAL",
    "CCGT",
    "INTNSL",
    "INTNEM",
    "INTIRL",
    "INTIFA2",
    "INTFR",
    "INTEW",
    "INTELEC",
    "INTNED",
}

required_locations = {
    location["location_name"] for location in locations
}

def create_live_dataset(session_elexon, session_open_meteo):
    demand = get_live_demand(
        session = session_elexon
    )

    if demand is None or demand.empty:
        raise ValueError(
            "No demand data was returned."
        )

    demand["start_time"] = pd.to_datetime(demand["start_time"], utc = True)

    generation = get_live_generation(
        session = session_elexon
    )

    if generation is None or generation.empty:
        raise ValueError(
            "No generation data was returned."
        )

    available_fules = set(generation["fuel_type"].unique())
    missing_fuels = required_fuels - available_fules
    if missing_fuels:
        raise ValueError(
            "Missing generation fuel types."
        )

    generation["publish_time"] = pd.to_datetime(generation["publish_time"], utc = True)
    generation["start_time"] = pd.to_datetime(generation["start_time"], utc = True)

    weather = get_live_weather_data(
        latitude = latitude,
        longitude = longitude,
        session = session_open_meteo
    )

    if weather is None or weather.empty:
        raise ValueError(
            "No weather data was returned."
        )

    available_locations = set(weather["location_name"].unique())
    missing_locations = required_locations - available_locations
    if missing_locations:
        raise ValueError(
            "Missing weather locations."
        )

    weather["forecast_time"] = pd.to_datetime(weather["forecast_time"], utc = True)

    latest_demand_time = demand["start_time"].max()
    latest_generation_time = generation["start_time"].max()
    current_time = pd.Timestamp.now(tz = "UTC")

    if current_time - latest_demand_time > pd.Timedelta(hours = 12):
        raise ValueError(
            "Latest demand data is more than 12 hours old."
        )

    if latest_demand_time != latest_generation_time:
        raise ValueError(
            "Latest demand and generation intervals are not aligned."
        )

    prediction_start = latest_demand_time + pd.Timedelta(minutes = 30)

    required_weather_times = pd.date_range(
        start = prediction_start.floor("h"),
        periods = 24,
        freq = "1h",
        tz = "UTC"
    )

    available_weather_times = set(weather["forecast_time"].unique())

    missing_weather_times = [
        time for time in required_weather_times
        if time not in available_weather_times
    ]

    if missing_weather_times:
        raise ValueError(
            f"Weather forecast is missing required times."
        )

    weather_counts = weather[
        weather["forecast_time"].isin(required_weather_times)
    ].groupby("forecast_time")["location_name"].nunique()
    invalid_weather_times = weather_counts[weather_counts != 8]

    if not invalid_weather_times.empty:
        raise ValueError(
            "Weather data is incomplete for one or more forecast hours."
        )

    future_row = pd.DataFrame({
        "start_time": [prediction_start],
        "true_demand_mw": [-1]
    })

    demand = pd.concat(
        [demand, future_row],
        ignore_index = True
    )

    demand = fill_demand_gaps(demand = demand)
    demand = half_day_lags(demand = demand)

    modelling = create_horizon_dataset(demand = demand)
    modelling.loc[modelling["reference_time"] == prediction_start, "target_demand"] = -1

    modelling = add_dynamic_demand_lags(modelling = modelling, demand = demand)
    modelling = modelling[modelling["reference_time"] == prediction_start].reset_index(drop = True)

    generation = fill_generation_gaps(generation = generation)
    generation = generation[
        (generation["fuel_type"] != "INTGRNL") 
        & (generation["fuel_type"] != "INTVKL")
    ]
    generation_pivot = pivot_generation(generation = generation)
    generation_pivot = add_generation_features(generation_pivot = generation_pivot)

    weather_pivot = pivot_weather(weather = weather)
    weather_pivot = add_weather_features(weather_pivot = weather_pivot)

    modelling = merge_with_modelling(
        modelling = modelling, 
        generation_pivot = generation_pivot, 
        weather_pivot = weather_pivot
    )
    modelling = add_time_features(modelling = modelling)

    missing_values = modelling.isna().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        raise ValueError(
            "Missing values found in modelling data."
        )

    expected_horizons = set(range(1, 49))
    actual_horizons = set(modelling["horizon"])
    if actual_horizons != expected_horizons:
        raise ValueError(
            "Expected 48 forecast horizons."
        )

    return modelling