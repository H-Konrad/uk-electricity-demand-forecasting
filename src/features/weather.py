import pandas as pd
import numpy as np

def pivot_weather(weather):
    weather = weather.drop(columns = "apparent_temperature")

    weather_pivot = weather.pivot(
        index = "forecast_time",
        columns = "location_name",
        values = [
            "temperature_2m",
            "relative_humidity_2m",
            "snowfall",
            "rain"
        ]
    ).reset_index()

    weather_pivot.columns = [
        f"{weather_condition}_{city}".lower().replace(" ", "_")
        for weather_condition, city in weather_pivot.columns
    ]

    return weather_pivot

def add_weather_features(weather_pivot):
    temperature_columns = [
        column for column in weather_pivot.columns
        if column.startswith("temp")
    ]

    rain_columns = [
        col for col in weather_pivot.columns
        if col.startswith("rain")
    ]

    snow_columns = [
        col for col in weather_pivot.columns
        if col.startswith("snow")
    ]

    weather_pivot["temperature_mean"] = weather_pivot[temperature_columns].mean(axis = 1)
    weather_pivot["temperature_min"] = weather_pivot[temperature_columns].min(axis = 1)
    weather_pivot["temperature_max"] = weather_pivot[temperature_columns].max(axis = 1)
    weather_pivot = weather_pivot.drop(columns = temperature_columns)

    weather_pivot["cities_with_rain"] = (weather_pivot[rain_columns] > 0).sum(axis = 1)
    weather_pivot["cities_with_snow"] = (weather_pivot[snow_columns] > 0).sum(axis = 1)

    weather_pivot[rain_columns] = np.log1p(weather_pivot[rain_columns])
    weather_pivot[snow_columns] = np.log1p(weather_pivot[snow_columns])

    weather_pivot = weather_pivot.rename(columns = {
        "forecast_time_": "target_time"
    })

    return weather_pivot