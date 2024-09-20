-- Add compression policies
ALTER MATERIALIZED VIEW daily_adjusted_prices set (timescaledb.compress = true);
SELECT add_compression_policy('daily_adjusted_prices', compress_after => INTERVAL '10 days');

ALTER MATERIALIZED VIEW daily_denom_prices set (timescaledb.compress = true);
SELECT add_compression_policy('daily_denom_prices', compress_after => INTERVAL '10 days');

ALTER MATERIALIZED VIEW daily_fx_prices set (timescaledb.compress = true);
SELECT add_compression_policy('daily_fx_prices', compress_after => INTERVAL '10 days');

ALTER MATERIALIZED VIEW daily_roll_calendars set (timescaledb.compress = true);
SELECT add_compression_policy('daily_roll_calendars', compress_after => INTERVAL '10 days');
