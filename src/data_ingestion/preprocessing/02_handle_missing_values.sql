UPDATE flight_data
SET geo_altitude = (SELECT AVG(geo_altitude) FROM flight_data)
WHERE geo_altitude IS NULL

UPDATE flight_data
SET baro_altitude = (SELECT AVG(baro_altitude) FROM flight_data)
WHERE baro_altitude IS NULL

DELETE FROM flight_data
WHERE latitude IS NULL OR longitude IS NULL OR time_position IS NULL;
