SELECT
	COUNT(*) AS total,
	COUNT(*) FILTER (WHERE publish_time IS NULL) AS null_publish,
	COUNT(*) FILTER (WHERE start_time IS NULL) AS null_start,
    COUNT(*) FILTER (WHERE generation_mw IS NULL) AS null_generation,
    COUNT(*) FILTER (WHERE fuel_type IS NULL) AS null_fuel_type
FROM generation;