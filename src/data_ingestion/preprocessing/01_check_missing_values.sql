SELECT 
    COUNT(*) FILTER (WHERE callsign IS NULL) AS missing_callsign,
    COUNT(*) FILTER (WHERE latitude IS NULL) AS missing_latitude,
    COUNT(*) FILTER (WHERE longitude IS NULL) AS missing_longitude,
    COUNT(*) FILTER (WHERE geo_altitude IS NULL) AS missing_geo_altitude,
    COUNT(*) FILTER (WHERE baro_altitude IS NULL) AS missing_baro_altitude,
    COUNT(*) FILTER (WHERE velocity IS NULL) AS missing_velocity,
    COUNT(*) FILTER (WHERE origin_country IS NULL) AS missing_origin_country,
    COUNT(*) FILTER (WHERE time_position IS NULL) AS missing_time_position,
    COUNT(*) FILTER (WHERE last_contact IS NULL) AS missing_last_contact
FROM flight_data;
