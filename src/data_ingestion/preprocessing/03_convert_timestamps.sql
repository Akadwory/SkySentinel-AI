-- Remove rows with invalid timestamps
DELETE FROM flight_data
WHERE time_position > (NOW() + INTERVAL '5 seconds')
   OR last_contact > (NOW() + INTERVAL '5 seconds');

-- Flag rows with zero velocity instead of immediate deletion
INSERT INTO flagged_data (SELECT * FROM flight_data WHERE velocity = 0);
DELETE FROM flight_data WHERE id IN (SELECT id FROM flagged_data);

-- Remove duplicate records based on callsign, timestamp, and spatial proximity
DELETE FROM flight_data a
USING flight_data b
WHERE a.id < b.id
AND a.callsign = b.callsign
AND a.time_position BETWEEN b.time_position - INTERVAL '1 second' AND b.time_position + INTERVAL '1 second'
AND earth_distance(ll_to_earth(a.latitude, a.longitude), ll_to_earth(b.latitude, b.longitude)) < 100;
