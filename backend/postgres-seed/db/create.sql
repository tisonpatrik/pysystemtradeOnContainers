DROP DATABASE IF EXISTS test_grayfox_db;
CREATE DATABASE test_grayfox_db;
\connect test_grayfox_db;

GRANT ALL PRIVILEGES ON DATABASE test_grayfox_db to "postgres";

DROP DATABASE IF EXISTS grayfox_db;
CREATE DATABASE grayfox_db;
\connect grayfox_db;

GRANT ALL PRIVILEGES ON DATABASE grayfox_db to "postgres";

\i /home/app/db/config_schemas.sql
\i /home/app/db/raw_data_schemas.sql
\i /home/app/db/risk_schemas.sql