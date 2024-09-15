-- Enable compression on roll_calendars table
ALTER TABLE roll_calendars
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Manually compress any existing chunks in roll_calendars
SELECT compress_chunk(c) FROM show_chunks('roll_calendars') c;

-- Add compression policy to compress chunks older than 7 days for roll_calendars
SELECT add_compression_policy('roll_calendars', INTERVAL '7 days');
