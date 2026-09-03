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