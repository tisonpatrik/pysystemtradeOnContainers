DROP DATABASE IF EXISTS grayfox_db;
CREATE DATABASE grayfox_db;
\connect grayfox_db;
CREATE SCHEMA shakespeare;
CREATE SCHEMA happy_hog;

DROP DATABASE IF EXISTS test_grayfox_db;
CREATE DATABASE test_grayfox_db;
\connect test_grayfox_db;
CREATE SCHEMA shakespeare;
CREATE SCHEMA happy_hog;
