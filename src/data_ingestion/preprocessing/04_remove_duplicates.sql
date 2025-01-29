DELETE FROM flight_data
WHERE id NOT IN (
    SELECT MIN(id)
    FROM flight_data
    GROUP BY callsign,latitude,longitude,time_position

);
