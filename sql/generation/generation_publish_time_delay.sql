SELECT
    fuel_type,
    CASE
		WHEN publish_time - start_time > INTERVAL '30 minutes' 
			THEN '> thirty'
		ELSE '<= thirty'
	END AS publish_delay,
    COUNT(*) AS count
FROM generation
WHERE source = 'FUELHH'
GROUP BY fuel_type, publish_delay
ORDER BY fuel_type, publish_delay;