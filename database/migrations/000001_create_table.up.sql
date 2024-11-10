BEGIN;

CREATE TABLE instrument_config (
    symbol VARCHAR PRIMARY KEY,
    description VARCHAR,
    pointsize NUMERIC(14, 3),
    currency VARCHAR,
    asset_class VARCHAR,
    per_block NUMERIC(14, 3),
    percentage NUMERIC(14, 3),
    per_trade INTEGER,
    region VARCHAR,
    tradable BOOLEAN
);

COMMIT;
