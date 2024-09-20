-- Drop continuous aggregate policy
SELECT remove_continuous_aggregate_policy('daily_adjusted_prices');
SELECT remove_continuous_aggregate_policy('daily_denom_prices');
SELECT remove_continuous_aggregate_policy('daily_fx_prices');
SELECT remove_continuous_aggregate_policy('daily_roll_calendars');
