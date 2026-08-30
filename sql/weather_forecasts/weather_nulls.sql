SELECT
	COUNT(*) FILTER (WHERE forecast_time IS NULL) AS null_forecast_time,
    COUNT(*) FILTER (WHERE temperature_2m IS NULL) AS null_temp,
    COUNT(*) FILTER (WHERE relative_humidity_2m IS NULL) AS null_humidity,
    COUNT(*) FILTER (WHERE apparent_temperature IS NULL) AS null_apparent_temp,
    COUNT(*) FILTER (WHERE snowfall IS NULL) AS null_snowfall,
    COUNT(*) FILTER (WHERE snowfall = 'NaN') AS nan_snowfall,
    COUNT(*) FILTER (WHERE rain IS NULL) AS null_rain,
    COUNT(*) FILTER (WHERE rain = 'NaN') AS nan_rain
FROM weather_forecasts;