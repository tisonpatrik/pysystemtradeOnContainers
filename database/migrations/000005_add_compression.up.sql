-- Enable compression on adjusted_prices table
ALTER TABLE adjusted_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Enable compression on fx_prices table
ALTER TABLE fx_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Enable compression on multiple_prices table
ALTER TABLE multiple_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Enable compression on roll_calendars table
ALTER TABLE roll_calendars
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Manually compress any existing chunks in all hypertables
SELECT compress_chunk(c) FROM show_chunks('adjusted_prices') c;
SELECT compress_chunk(c) FROM show_chunks('fx_prices') c;
SELECT compress_chunk(c) FROM show_chunks('multiple_prices') c;
SELECT compress_chunk(c) FROM show_chunks('roll_calendars') c;

-- Add compression policy to compress chunks older than 7 days
SELECT add_compression_policy('adjusted_prices', INTERVAL '7 days');
SELECT add_compression_policy('fx_prices', INTERVAL '7 days');
SELECT add_compression_policy('multiple_prices', INTERVAL '7 days');
SELECT add_compression_policy('roll_calendars', INTERVAL '7 days');
