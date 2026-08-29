WITH
	time_intervals AS (
		SELECT
			fuel_type,
			publish_time,
			LAG(publish_time) OVER (
				PARTITION BY fuel_type ORDER BY publish_time
			) AS previous_publish,
			generation_mw,
			LAG(generation_mw) OVER (
				PARTITION BY fuel_type ORDER BY start_time
			) AS previous_generation,
			start_time - LAG(start_time) OVER (
				PARTITION BY fuel_type ORDER BY start_time
			) AS interval
		FROM generation
	)
SELECT
	*
FROM time_intervals
WHERE interval = INTERVAL '0 minutes'
ORDER BY fuel_type, publish_time;