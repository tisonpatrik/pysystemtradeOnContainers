-- Remove compression policy from roll_calendars
SELECT remove_compression_policy('roll_calendars');

-- Disable compression on roll_calendars table
ALTER TABLE roll_calendars
SET (
    timescaledb.compress = false
);
