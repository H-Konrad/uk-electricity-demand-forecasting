import pandas as pd
import numpy as np

fuels = [
    "BIOMASS",
    "WIND",
    "PS",
    "OTHER",
    "OCGT",
    "NPSHYD",
    "NUCLEAR",
    "COAL",
    "CCGT"
]

interconnectors = [
    "INTNSL",
    "INTNEM",
    "INTIRL",
    "INTIFA2",
    "INTFR",
    "INTEW",
    "INTELEC",
    "INTNED"
]

def fill_generation_gaps(generation):
    complete_data = []

    for fuel_type, df in generation.groupby("fuel_type"):
        df = df.sort_values("start_time").set_index("start_time")

        timeline = pd.date_range(
            start = df.index.min(),
            end = df.index.max(),
            freq = "30min",
            tz = df.index.tz
        )

        df = df.reindex(timeline)
        df["fuel_type"] = fuel_type
        df["generation_mw"] = df["generation_mw"].interpolate(
            method = "linear", 
            limit = 4, 
            limit_area = "inside"
        )
        df["publish_time"] = df["publish_time"].fillna(pd.Series(
            df.index + pd.Timedelta(minutes = 30), 
            index = df.index
        ))
        df = df.rename_axis("start_time").reset_index()

        complete_data.append(df)

    generation = pd.concat(
        complete_data,
        ignore_index = True
    ).sort_values("start_time")

    return generation

def pivot_generation(generation):
    generation_pivot = generation.pivot_table(
        index = "publish_time",
        columns = "fuel_type",
        values = "generation_mw",
        aggfunc = "last"
    ).reset_index().sort_values("publish_time").drop(columns = "OIL")

    return generation_pivot

def add_generation_features(generation_pivot):
    generation_pivot["total_fuel"] = generation_pivot[fuels].sum(axis = 1)
    generation_pivot["total_interconnector"] = generation_pivot[interconnectors].sum(axis = 1)
    generation_pivot["total_generation"] = generation_pivot["total_fuel"] + generation_pivot["total_interconnector"]

    generation_pivot["OTHER"] = np.log1p(generation_pivot["OTHER"])
    generation_pivot["OCGT"] = np.log1p(generation_pivot["OCGT"])
    generation_pivot["NPSHYD"] = np.log1p(generation_pivot["NPSHYD"])
    generation_pivot["COAL"] = np.log1p(generation_pivot["COAL"])
    generation_pivot["CCGT"] = np.log1p(generation_pivot["CCGT"])

    generation_pivot["INTNSL"] = np.sign(generation_pivot["INTNSL"]) * np.log1p(np.abs(generation_pivot["INTNSL"]))
    generation_pivot["INTNEM"] = np.sign(generation_pivot["INTNEM"]) * np.log1p(np.abs(generation_pivot["INTNEM"]))

    features_for_lag = fuels + interconnectors + ["total_fuel", "total_interconnector", "total_generation"]

    for feature in features_for_lag:
        generation_pivot[f"{feature}_lag_30m"] = generation_pivot[feature].shift(1)
        generation_pivot[f"{feature}_lag_1h"] = generation_pivot[feature].shift(2)
        generation_pivot[f"{feature}_lag_2h"] = generation_pivot[feature].shift(4)

    generation_pivot = generation_pivot.rename(columns = {
        "publish_time": "reference_time"
    })

    return generation_pivot