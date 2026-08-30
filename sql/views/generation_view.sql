CREATE VIEW generation_eda AS
SELECT
	publish_time,
    start_time,
    fuel_type,
    generation_mw
FROM generation
WHERE fuel_type != 'INTGRNL'
	OR source != 'AGWS'