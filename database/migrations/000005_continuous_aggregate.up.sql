-- Create continuous aggregate view for hypertables
CREATE MATERIALIZED VIEW daily_adjusted_prices
WITH (timescaledb.continuous) AS
SELECT
  symbol,
  time_bucket(INTERVAL '1 day', time) AS day_bucket,
  last(price, time) AS last_price
FROM adjusted_prices
GROUP BY symbol, day_bucket
WITH NO DATA;

CREATE MATERIALIZED VIEW daily_denom_prices
WITH (timescaledb.continuous) AS
SELECT
  symbol,
  time_bucket(INTERVAL '1 day', time) AS day_bucket,
  last(price, time) AS last_price
FROM multiple_prices
GROUP BY symbol, day_bucket
WITH NO DATA;

CREATE MATERIALIZED VIEW daily_fx_prices
WITH (timescaledb.continuous) AS
SELECT
  symbol,
  time_bucket(INTERVAL '1 day', time) AS day_bucket,
  last(price, time) AS last_price
FROM fx_prices
GROUP BY symbol, day_bucket
WITH NO DATA;

CREATE MATERIALIZED VIEW daily_roll_calendars
WITH (timescaledb.continuous) AS
SELECT
  symbol,
  time_bucket(INTERVAL '1 day', time) AS day_bucket,
  last(current_contract, time) AS last_current_contract,
  last(next_contract, time) AS last_next_contract,
  last(carry_contract, time) AS last_carry_contract
FROM roll_calendars
GROUP BY symbol, day_bucket
WITH NO DATA;
