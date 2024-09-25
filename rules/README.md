WITH last_non_null_prices AS (
  SELECT
    symbol,
    time_bucket(INTERVAL '1 day', time) AS day_bucket,
    MAX(time) FILTER (WHERE price IS NOT NULL) AS last_non_null_time
  FROM
    adjusted_prices
  WHERE
    symbol = 'AEX'
    AND EXTRACT(ISODOW FROM time) BETWEEN 1 AND 5  -- Filtruje pondělí až pátek
  GROUP BY
    symbol,
    day_bucket
)
SELECT
  l.symbol,
  l.day_bucket,
  ap.price AS last_price
FROM
  last_non_null_prices l
JOIN
  adjusted_prices ap
  ON l.symbol = ap.symbol
  AND time_bucket(INTERVAL '1 day', ap.time) = l.day_bucket
  AND ap.time = l.last_non_null_time
ORDER BY
  l.symbol,
  l.day_bucket;



  CREATE MATERIALIZED VIEW daily_denom_prices
  WITH (timescaledb.continuous) AS
  SELECT
    l.symbol,
    l.day_bucket,
    ap.price AS last_price
  FROM (
    SELECT
      symbol,
      time_bucket(INTERVAL '1 day', time) AS day_bucket,
      MAX(time) FILTER (WHERE price IS NOT NULL) AS last_non_null_time
    FROM
      multiple_prices
    WHERE
      EXTRACT(ISODOW FROM time) BETWEEN 1 AND 5  -- Filtruje pondělí až pátek
    GROUP BY
      symbol,
      day_bucket
  ) l
  JOIN
    multiple_prices ap
    ON l.symbol = ap.symbol
    AND time_bucket(INTERVAL '1 day', ap.time) = l.day_bucket
    AND ap.time = l.last_non_null_time
  ORDER BY
    l.symbol,
    l.day_bucket
  WITH NO DATA;
