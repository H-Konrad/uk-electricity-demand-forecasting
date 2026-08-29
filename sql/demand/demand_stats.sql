SELECT
	MIN(true_demand_mw) AS min_demand,
	MAX(true_demand_mw) AS max_demand,
	AVG(true_demand_mw) AS avg_demand
FROM demand;