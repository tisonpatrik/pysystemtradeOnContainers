CREATE TABLE instrument_config (
    symbol VARCHAR(50) PRIMARY KEY, 
    description TEXT, 
    pointsize FLOAT, 
    currency VARCHAR(10), 
    asset_class VARCHAR(50), 
    per_block FLOAT, 
    percentage FLOAT, 
    per_trade INTEGER, 
    region VARCHAR(50)
)
