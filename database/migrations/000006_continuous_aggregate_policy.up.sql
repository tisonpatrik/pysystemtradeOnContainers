
-- Add continuous aggregate policy to refresh every day
SELECT add_continuous_aggregate_policy('daily_adjusted_prices',
start_offset => INTERVAL '7 days',
end_offset   => INTERVAL '1 day',
schedule_interval => INTERVAL '1 day');

SELECT add_continuous_aggregate_policy('daily_denom_prices',
start_offset => INTERVAL '7 days',
end_offset   => INTERVAL '1 day',
schedule_interval => INTERVAL '1 day');

SELECT add_continuous_aggregate_policy('daily_fx_prices',
start_offset => INTERVAL '7 days',
end_offset   => INTERVAL '1 day',
schedule_interval => INTERVAL '1 day');


SELECT add_continuous_aggregate_policy('daily_roll_calendars',
start_offset => INTERVAL '7 days',
end_offset   => INTERVAL '1 day',
schedule_interval => INTERVAL '1 day');
