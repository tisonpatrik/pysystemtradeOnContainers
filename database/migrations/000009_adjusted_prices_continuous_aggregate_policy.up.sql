-- Create continuous aggregate view for adjusted_prices
CREATE MATERIALIZED VIEW daily_adjusted_prices
WITH (timescaledb.continuous) AS
SELECT
  symbol,
  time_bucket(INTERVAL '1 day', time) AS day_bucket,
  last(price, time) AS last_price
FROM adjusted_prices
GROUP BY symbol, day_bucket;

-- Add continuous aggregate policy to refresh every hour
SELECT add_continuous_aggregate_policy('daily_adjusted_prices',
  start_offset => INTERVAL '1 month',
  end_offset   => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 hour');
