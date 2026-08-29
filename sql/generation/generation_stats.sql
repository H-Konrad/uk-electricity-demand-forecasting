SELECT
    fuel_type,
    COUNT(*) AS total,
    MIN(generation_mw) AS min_generation,
    MAX(generation_mw) AS max_generation,
	AVG(generation_mw) AS avg_generation
FROM generation
GROUP BY fuel_type
ORDER BY total DESC;