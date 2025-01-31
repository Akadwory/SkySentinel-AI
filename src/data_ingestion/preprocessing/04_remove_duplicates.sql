DELETE FROM flight_data a
USING (
    SELECT MIN(id) AS id, callsign, latitude, longitude, time_position
    FROM flight_data
    GROUP BY callsign, latitude, longitude, time_position
) b
WHERE a.id <> b.id
AND a.callsign = b.callsign
AND a.latitude = b.latitude
AND a.longitude = b.longitude
AND a.time_position = b.time_position;
