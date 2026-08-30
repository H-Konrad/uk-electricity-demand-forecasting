WITH
	time_intervals AS (
	    SELECT
	        l.location_name,
	        wf.forecast_time,
	        wf.forecast_time - LAG(wf.forecast_time)
	            OVER (
	                PARTITION BY l.location_name
	                ORDER BY wf.forecast_time
	            ) AS interval
	    FROM weather_forecasts wf
		LEFT JOIN locations l
			ON l.location_id = wf.location_id
	)
SELECT
	*
FROM time_intervals
WHERE interval != INTERVAL '1 hour';