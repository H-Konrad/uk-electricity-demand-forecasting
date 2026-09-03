import pandas as pd

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
