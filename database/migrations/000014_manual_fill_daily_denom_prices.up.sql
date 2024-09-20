-- Manual refresh for continuous aggregate views
CALL refresh_continuous_aggregate('daily_denom_prices', NULL, localtimestamp - INTERVAL '7 days');
