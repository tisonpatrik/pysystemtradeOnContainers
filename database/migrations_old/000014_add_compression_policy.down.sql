-- Disable compression for the continuous aggregate view
ALTER MATERIALIZED VIEW daily_adjusted_prices SET (timescaledb.compress = false);

ALTER MATERIALIZED VIEW daily_denom_prices SET (timescaledb.compress = false);
