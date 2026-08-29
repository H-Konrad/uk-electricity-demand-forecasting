SELECT
    COUNT(*) AS total_rows,
	COUNT(*) FILTER (WHERE publish_time IS NULL) AS null_publish,
	COUNT(*) FILTER (WHERE start_time IS NULL) AS null_start,
    COUNT(*) FILTER (WHERE true_demand_mw IS NULL) AS null_demand
FROM demand;