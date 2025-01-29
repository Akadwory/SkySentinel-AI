UPDATE flight_data
SET callsign = TRIM(BOTH ' ' FROM callsign)