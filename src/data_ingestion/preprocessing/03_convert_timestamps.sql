DELETE FROM flight_data
WHERE latitude IS NULL OR longitude IS NULL OR time_position IS NULL OR last_contact IS NULL;

DELETE FROM flight_data
WHERE time_position > NOW() OR last_contact > NOW();


DELETE FROM flight_data a
USING flight_data b
WHERE a.id < b.id
AND a.callsign = b.callsign
AND a.time_position = b.time_position;


DELETE FROM flight_data
WHERE velocity = 0;
