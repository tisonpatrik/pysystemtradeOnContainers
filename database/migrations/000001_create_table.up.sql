CREATE TABLE instrument_config (
    symbol VARCHAR PRIMARY KEY,
    description VARCHAR,
    pointsize FLOAT,
    currency VARCHAR,
    asset_class VARCHAR,
    per_block FLOAT,
    percentage FLOAT,
    per_trade INTEGER,
    region VARCHAR
);

CREATE TABLE instrument_metadata (
    symbol VARCHAR PRIMARY KEY,
    asset_class VARCHAR,
    sub_class VARCHAR,
    CONSTRAINT fk_symbol FOREIGN KEY(symbol) REFERENCES instrument_config(symbol)
);

CREATE TABLE roll_config (
    symbol VARCHAR PRIMARY KEY,
    hold_roll_cycle VARCHAR,
    roll_offset_days INTEGER,
    carry_offset INTEGER,
    priced_roll_cycle VARCHAR,
    expiry_offset INTEGER,
    CONSTRAINT fk_symbol_roll FOREIGN KEY(symbol) REFERENCES instrument_config(symbol)
);

CREATE TABLE spread_costs (
    symbol VARCHAR PRIMARY KEY,
    spread_costs FLOAT,
    CONSTRAINT fk_symbol_spread FOREIGN KEY(symbol) REFERENCES instrument_config(symbol)
);
