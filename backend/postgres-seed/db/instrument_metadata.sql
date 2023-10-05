CREATE TABLE instrument_metadata (
                    symbol VARCHAR(50) PRIMARY KEY,
                    asset_class VARCHAR(50),
                    sub_class VARCHAR(50),
                    sub_sub_class VARCHAR(50),
                    description VARCHAR(100)
                )