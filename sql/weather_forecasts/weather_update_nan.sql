UPDATE 
	weather_forecasts
SET
    snowfall = CASE WHEN snowfall = 'NaN' THEN '0' ELSE snowfall END,
    rain = CASE WHEN rain = 'NaN' THEN '0' ELSE rain END
WHERE snowfall = 'NaN'
   OR rain = 'NaN';