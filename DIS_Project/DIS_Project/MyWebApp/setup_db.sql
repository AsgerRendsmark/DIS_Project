CREATE TABLE IF NOT EXISTS users (
id  SERIAL PRIMARY KEY, 
email VARCHAR(255), 
first_name VARCHAR(255), 
password VARCHAR(255));

CREATE TABLE IF NOT EXISTS stocks1 (
id SERIAL PRIMARY KEY,
symbol VARCHAR(255),
name VARCHAR(255),
shares INTEGER,
price NUMERIC(10,2),
total NUMERIC(10,2),
CONSTRAINT stocks1_id_unique UNIQUE (id));

CREATE TABLE IF NOT EXISTS favorites (
id INTEGER PRIMARY KEY,
user_id INTEGER,
stock_id INTEGER,
CONSTRAINT unique_user_stock UNIQUE (user_id, stock_id),
FOREIGN KEY (user_id) REFERENCES users (id),
FOREIGN KEY (stock_id) REFERENCES stocks1 (id));

CREATE TABLE IF NOT EXISTS stock_history (
stock_id INTEGER,   
name VARCHAR(255),
date VARCHAR(255),
open_price FLOAT,
high_price FLOAT,
low_price FLOAT,
close_price FLOAT,
volume BIGINT,
FOREIGN KEY (stock_id) REFERENCES stocks1 (id));