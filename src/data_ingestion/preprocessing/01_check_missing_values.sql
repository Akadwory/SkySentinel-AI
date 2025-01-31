-- Script to check missing or problematic data
SELECT 
    COUNT(*) FILTER (WHERE callsign IS NULL) AS missing_callsign,
    COUNT(*) FILTER (WHERE latitude IS NULL) AS missing_latitude,
    COUNT(*) FILTER (WHERE longitude IS NULL) AS missing_longitude,
    COUNT(*) FILTER (WHERE geo_altitude IS NULL) AS missing_geo_altitude,
    COUNT(*) FILTER (WHERE baro_altitude IS NULL) AS missing_baro_altitude,
    COUNT(*) FILTER (WHERE velocity IS NULL OR velocity < 5) AS problematic_velocity,
    COUNT(*) FILTER (WHERE origin_country IS NULL) AS missing_origin_country,
    COUNT(*) FILTER (WHERE time_position IS NULL OR last_contact IS NULL) AS missing_timestamps
FROM flight_data;

-- Output sample statistics to keep track of data health
