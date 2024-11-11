BEGIN;

CREATE TABLE instrument_config (
    symbol VARCHAR PRIMARY KEY,
    description VARCHAR,
    pointsize NUMERIC(18, 5),
    currency VARCHAR,
    asset_class VARCHAR,
    per_block NUMERIC(14, 9),
    percentage NUMERIC(7, 5),
    per_trade INTEGER,
    region VARCHAR,
    is_tradable BOOLEAN,
    have_data BOOLEAN
);

COMMIT;
