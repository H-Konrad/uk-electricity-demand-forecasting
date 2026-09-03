import pandas as pd

def get_demand_df(conn):
    query = """
        SELECT 
            *
        FROM demand_eda
        ORDER BY start_time;
    """

    demand = pd.read_sql(query, conn)
    demand["start_time"] = pd.to_datetime(demand["start_time"], utc = True)

    return demand

def get_generation_df(conn):
    query = """
        SELECT *
        FROM generation_eda
        ORDER BY start_time;
    """

    generation = pd.read_sql(query, conn)
    generation["publish_time"] = pd.to_datetime(generation["publish_time"], utc = True)
    generation["start_time"] = pd.to_datetime(generation["start_time"], utc = True)

    return generation

def get_weather_df(conn):
    query = """
        SELECT *
        FROM weather_eda
        ORDER BY forecast_time;
    """

    weather = pd.read_sql(query, conn)
    weather["forecast_time"] = pd.to_datetime(weather["forecast_time"], utc = True)

    return weather