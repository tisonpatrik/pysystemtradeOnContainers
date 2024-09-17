-- Create continuous aggregate view for multiple_prices
CREATE MATERIALIZED VIEW daily_denom_prices
WITH (timescaledb.continuous) AS
SELECT
  symbol,
  time_bucket(INTERVAL '1 day', time) AS day_bucket,
  last(price, time) AS last_price
FROM multiple_prices
GROUP BY symbol, day_bucket;
