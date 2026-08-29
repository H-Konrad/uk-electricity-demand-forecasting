WITH
	time_intervals AS (
		SELECT
			fuel_type,
			start_time - LAG(start_time) OVER (
				PARTITION BY fuel_type ORDER BY start_time
			) AS interval
		FROM generation
	)
SELECT
    *,
    COUNT(*) AS total
FROM time_intervals
WHERE interval != INTERVAL '30 minutes'
GROUP BY fuel_type, interval
ORDER BY total DESC, interval DESC, fuel_type;