-- Retrieve a sample of the processed data for validation and further analysis
SELECT * FROM flight_data
ORDER BY time_position DESC
LIMIT 1000;

-- Optional: Output statistics for debugging purposes
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT callsign) AS unique_callsigns,
    COUNT(*) FILTER (WHERE velocity = 0) AS stalled_flights,
    COUNT(*) FILTER (WHERE geo_altitude < 500 OR baro_altitude < 500) AS low_altitude_flights
FROM flight_data;
