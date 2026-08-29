WITH
	time_intervals AS (
		SELECT
			fuel_type,
			start_time,
			publish_time,
			start_time - LAG(start_time) OVER (
				PARTITION BY fuel_type ORDER BY start_time
			) AS interval
		FROM generation
		WHERE source = 'FUELHH'
	)
SELECT
	*
FROM time_intervals
WHERE interval != INTERVAL '30 minutes';