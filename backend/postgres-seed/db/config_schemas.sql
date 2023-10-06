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
                    );

CREATE TABLE instrument_metadata (
                    symbol VARCHAR(50) PRIMARY KEY,
                    asset_class VARCHAR(50),
                    sub_class VARCHAR(50),
                    sub_sub_class VARCHAR(50),
                    description VARCHAR(100)
                );

CREATE TABLE roll_config (
                    symbol VARCHAR(50) PRIMARY KEY,
                    hold_roll_cycle VARCHAR(50),
                    roll_offset_days INTEGER,
                    carry_offset INTEGER,
                    priced_roll_cycle VARCHAR(50),
                    expiry_offset INTEGER
                );

CREATE TABLE spread_cost (
                    symbol VARCHAR(50) PRIMARY KEY,
                    spread_cost FLOAT
                );