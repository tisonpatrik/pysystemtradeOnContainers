-- Drop continuous aggregate policy
SELECT remove_continuous_aggregate_policy('daily_adjusted_prices');

-- Drop the continuous aggregate view
DROP MATERIALIZED VIEW IF EXISTS daily_adjusted_prices;
