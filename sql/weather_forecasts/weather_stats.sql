SELECT
    l.location_name,
    COUNT(*) AS row_count,
	
    MIN(temperature_2m) AS max_temp,
    MAX(temperature_2m) AS min_temp,
	AVG(temperature_2m) AS avg_temp,
	
    MIN(relative_humidity_2m) AS max_humidity,
    MAX(relative_humidity_2m) AS min_humidity,
	AVG(relative_humidity_2m) AS avg_humidity,    
	
	MIN(apparent_temperature) AS max_apparent_temp,
    MAX(apparent_temperature) AS min_apparent_temp,
	AVG(apparent_temperature) AS avg_apparent_temp,   
	
	MIN(NULLIF(wf.snowfall, 'NaN')) AS min_snowfall,
	MAX(NULLIF(wf.snowfall, 'NaN')) AS max_snowfall,
	AVG(NULLIF(wf.snowfall, 'NaN')) AS avg_snowfall,
	
	MIN(NULLIF(wf.rain, 'NaN')) AS min_rain,
	MAX(NULLIF(wf.rain, 'NaN')) AS max_rain,
	AVG(NULLIF(wf.rain, 'NaN')) AS avg_rain
FROM weather_forecasts wf
LEFT JOIN locations l 
	ON wf.location_id = l.location_id
WHERE wf.temperature_2m IS NOT NULL
  AND wf.relative_humidity_2m IS NOT NULL
  AND wf.apparent_temperature IS NOT NULL
  AND wf.snowfall IS NOT NULL
  AND wf.rain IS NOT NULL
GROUP BY l.location_name
ORDER BY l.location_name;