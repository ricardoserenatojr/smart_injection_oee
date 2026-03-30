CREATE DATABASE IF NOT EXISTS factory_db;
USE factory_db;

-- Production Log
CREATE TABLE IF NOT EXISTS production_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    line_id VARCHAR(50),
    operator_name VARCHAR(100),
    good_units INT,
    defective_units INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Downtime Log
CREATE TABLE IF NOT EXISTS downtime_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    line_id VARCHAR(50),
    reason VARCHAR(100),
    duration_min INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);