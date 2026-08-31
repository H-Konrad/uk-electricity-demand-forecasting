CREATE VIEW generation_eda AS
SELECT
	publish_time,
    start_time,
    fuel_type,
    generation_mw
FROM generation
WHERE fuel_type NOT IN ('INTGRNL', 'INTVKL')
	AND source != 'AGWS'