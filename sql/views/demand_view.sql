CREATE VIEW demand_eda AS
SELECT
    start_time,
    true_demand_mw
FROM demand
ORDER BY start_time;