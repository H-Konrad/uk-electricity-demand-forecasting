CREATE VIEW weather_eda AS
SELECT
    l.location_name,
    wf.forecast_time,
    wf.temperature_2m,
    wf.relative_humidity_2m,
    wf.apparent_temperature,
    wf.snowfall,
    wf.rain
FROM weather_forecasts wf
LEFT JOIN locations l 
	ON l.location_id = wf.location_id
ORDER BY forecast_time;