from src.features.demand import fill_demand_gaps, half_day_lags
from src.features.generation import fill_generation_gaps, pivot_generation, add_generation_features
from src.features.weather import pivot_weather, add_weather_features
from src.features.modelling import (
    create_horizon_dataset, add_dynamic_demand_lags, merge_with_modelling, add_time_features
)
from src.database.database_to_pandas import get_demand_df, get_generation_df, get_weather_df
from src.database.connection import get_connection

def main():
    conn = get_connection()

    demand = get_demand_df(conn)
    generation = get_generation_df(conn)
    weather = get_weather_df(conn)

    demand = fill_demand_gaps(demand)
    demand = half_day_lags(demand)

    modelling = create_horizon_dataset(demand)
    modelling = add_dynamic_demand_lags(modelling, demand)

    generation = fill_generation_gaps(generation)
    generation_pivot = pivot_generation(generation)
    generation_pivot = add_generation_features(generation_pivot)

    weather_pivot = pivot_weather(weather)
    weather_pivot = add_weather_features(weather_pivot)

    modelling = merge_with_modelling(modelling, generation_pivot, weather_pivot)
    modelling = add_time_features(modelling)

    modelling.to_parquet("data/modelling_dataset.parquet", index = False, engine = "pyarrow")

    print(modelling.shape)

if __name__ == "__main__":
    main()