DO $$
DECLARE
    batch_size INT := 1000;
BEGIN
    LOOP
        -- Update rows in manageable batches to reduce lock duration
        UPDATE flight_data
        SET callsign = TRIM(callsign)
        WHERE id IN (
            SELECT id FROM flight_data
            WHERE callsign IS NOT NULL
            AND (callsign LIKE ' %' OR callsign LIKE '% ' OR callsign LIKE '%\t%' OR callsign LIKE '%\n%')
            LIMIT batch_size
        );

        -- Exit loop if no rows were updated
        IF NOT FOUND THEN
            EXIT;
        END IF;
    END LOOP;
END $$;
