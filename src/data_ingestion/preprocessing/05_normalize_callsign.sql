DO $$
DECLARE
    batch_size INT := 1000;
BEGIN
    LOOP
        -- Update callsign field by removing any non-alphanumeric characters
        UPDATE flight_data
        SET callsign = REGEXP_REPLACE(TRIM(callsign), '[^a-zA-Z0-9]', '', 'g')
        WHERE id IN (
            SELECT id FROM flight_data
            WHERE callsign IS NOT NULL
            AND (callsign LIKE ' %' OR callsign LIKE '% ' OR callsign LIKE '%\t%' OR callsign LIKE '%\n%' OR callsign ~ '[^a-zA-Z0-9]')
            LIMIT batch_size
        );

        -- Exit loop if no rows were updated
        IF NOT FOUND THEN
            EXIT;
        END IF;
    END LOOP;
END $$;
