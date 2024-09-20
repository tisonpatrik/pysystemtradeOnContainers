-- Manual refresh for continuous aggregate views
CALL refresh_continuous_aggregate('daily_roll_calendars', NULL, localtimestamp - INTERVAL '7 days');
