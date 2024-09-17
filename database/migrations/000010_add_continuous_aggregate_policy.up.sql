
-- Add continuous aggregate policy to refresh every day
SELECT add_continuous_aggregate_policy('daily_adjusted_prices',
  start_offset => INTERVAL '1 month',
  end_offset   => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 day');
