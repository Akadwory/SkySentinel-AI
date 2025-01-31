-- Handle missing altitude data using country-based averages instead of global averages
UPDATE flight_data
SET geo_altitude = (
    SELECT AVG(geo_altitude) 
    FROM flight_data AS grouped
    WHERE grouped.origin_country = flight_data.origin_country
)
WHERE geo_altitude IS NULL;

UPDATE flight_data
SET baro_altitude = (
    SELECT AVG(baro_altitude) 
    FROM flight_data AS grouped
    WHERE grouped.origin_country = flight_data.origin_country
)
WHERE baro_altitude IS NULL;

-- Move incomplete data to a flagged table instead of deleting
CREATE TABLE IF NOT EXISTS flagged_data AS TABLE flight_data WITH NO DATA;

INSERT INTO flagged_data (SELECT * FROM flight_data WHERE latitude IS NULL OR longitude IS NULL OR time_position IS NULL);
DELETE FROM flight_data WHERE id IN (SELECT id FROM flagged_data);
