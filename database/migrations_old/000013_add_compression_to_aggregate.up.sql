-- Enable compression for the continuous aggregate view
ALTER MATERIALIZED VIEW daily_adjusted_prices SET (timescaledb.compress = true);

ALTER MATERIALIZED VIEW daily_denom_prices SET (timescaledb.compress = true);
