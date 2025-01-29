ALTER TABLE flight_data
ALTER COLUMN time_position TYPE TIMESTAMP USING TO_TIMESTAMP(time_position);

ALTER TABLE flight_data
ALTER COLUMN last_contact TYPE TIMESTAMP USING TO_TIMESTAMP(last_contact);