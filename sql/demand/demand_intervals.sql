WITH 
	interval_times AS (
		SELECT
		    start_time,
		    start_time - LAG(start_time) OVER (ORDER BY start_time) AS interval
		FROM demand
	)
SELECT 
	*
FROM interval_times
WHERE interval != INTERVAL '30 minutes';