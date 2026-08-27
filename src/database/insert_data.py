from src.database.connection import get_connection

class InsertToDatabase:
    def __init__(self):
        self.conn = get_connection()

    def insert_demand(self, rows):
        query = """
            INSERT INTO demand (
                publish_time,
                start_time,
                demand_mw
            )
            VALUES (
                %(publish_time)s,
                %(start_time)s,
                %(demand_mw)s
            )
            ON CONFLICT DO NOTHING;
        """

        with self.conn.cursor() as cursor:
            cursor.executemany(query, rows)

        self.conn.commit()

    def insert_generation(self, rows):
        query = """
            INSERT INTO generation (
                source,
                publish_time,
                start_time,
                fuel_type,
                generation_mw
            )
            VALUES (
                %(source)s,
                %(publish_time)s,
                %(start_time)s,
                %(fuel_type)s,
                %(generation_mw)s
            )
            ON CONFLICT DO NOTHING;
        """

        with self.connection.cursor() as cursor:
            cursor.executemany(query, rows)

        self.connection.commit()

    def insert_ndf(self, rows):
        query = """
            INSERT INTO ndf (
                publish_time,
                forecast_time,
                forecast_demand_mw
            )
            VALUES (
                %(publish_time)s,
                %(forecast_time)s,
                %(forecast_demand_mw)s
            )
            ON CONFLICT DO NOTHING;
        """

        with self.connection.cursor() as cursor:
            cursor.executemany(query, rows)

        self.connection.commit()

    def insert_ndfd(self, rows):
        query = """
            INSERT INTO ndfd (
                publish_time,
                forecast_date,
                forecast_demand_mw
            )
            VALUES (
                %(publish_time)s,
                %(forecast_date)s,
                %(forecast_demand_mw)s
            )
            ON CONFLICT DO NOTHING;
        """

        with self.connection.cursor() as cursor:
            cursor.executemany(query, rows)

        self.connection.commit()

    def insert_weather(self, rows):
        query = """
            INSERT INTO weather_forecasts (
                location_id,
                forecast_time,
                temperature_2m,
                relative_humidity_2m,
                apparent_temperature,
                snowfall,
                rain,
                showers,
                weather_code
            )
            VALUES (
                %(location_id)s,
                %(forecast_time)s,
                %(temperature_2m)s,
                %(relative_humidity_2m)s,
                %(apparent_temperature)s,
                %(snowfall)s,
                %(rain)s,
                %(showers)s,
                %(weather_code)s
            )
            ON CONFLICT DO NOTHING;
        """

        with self.connection.cursor() as cursor:
            cursor.executemany(query, rows)

        self.connection.commit()

    def insert_locations(self, rows):

        query = """
            INSERT INTO locations (
                location_id,
                location_name,
                latitude,
                longitude
            )
            VALUES (
                %(location_id)s,
                %(location_name)s,
                %(latitude)s,
                %(longitude)s
            )
            ON CONFLICT DO NOTHING;
        """

        with self.conn.cursor() as cursor:
            cursor.executemany(query, rows)

        self.conn.commit()

    def close(self):
        self.conn.close()
