-- Add compression policy for continuous aggregate view
-- Ensure that the compress_after interval is larger than the start_offset of the refresh policy
SELECT add_compression_policy('daily_adjusted_prices', compress_after => INTERVAL '14 days');

SELECT add_compression_policy('daily_denom_prices', compress_after => INTERVAL '14 days');
