-- Create adjusted_prices table without indexes
CREATE TABLE adjusted_prices (
    time TIMESTAMPTZ NOT NULL,
    price DOUBLE PRECISION NULL,
    symbol TEXT NOT NULL,
    PRIMARY KEY (time, symbol)
);

-- Create fx_prices table without indexes
CREATE TABLE fx_prices (
    time TIMESTAMPTZ NOT NULL,
    price DOUBLE PRECISION NULL,
    symbol TEXT NOT NULL,
    PRIMARY KEY (time, symbol)
);

-- Create multiple_prices table without indexes
CREATE TABLE multiple_prices (
    time TIMESTAMPTZ NOT NULL,
    carry DOUBLE PRECISION NULL,
    carry_contract INTEGER NOT NULL,
    price DOUBLE PRECISION NULL,
    price_contract INTEGER NOT NULL,
    forward DOUBLE PRECISION NULL,
    forward_contract INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    PRIMARY KEY (time, symbol)
);

-- Create roll_calendars table without indexes
CREATE TABLE roll_calendars (
    time TIMESTAMPTZ NOT NULL,
    current_contract INTEGER NOT NULL,
    next_contract INTEGER NOT NULL,
    carry_contract INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    PRIMARY KEY (time, symbol)
);
