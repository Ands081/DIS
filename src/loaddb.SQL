CREATE TABLE IF NOT EXISTS kebabshop(
kid integer PRIMARY KEY,
name varchar(100),
address text,
rating float(2),
x_coordinate real,
y_coordinate real,
tlfnr text);

CREATE TABLE IF NOT EXISTS reviews(
rid integer PRIMARY KEY,
kid integer,
rating float(2),
review text);

CREATE TABLE IF NOT EXISTS distance(
kid integer PRIMARY KEY,
dist text);

copy kebabshop(kid, name, address, rating, x_coordinate, y_coordinate, tlfnr)
            from 'C:\Users\Peter\Desktop\Durum\src\database\kebabshop.csv'
            delimiter ','
            CSV HEADER
            ENCODING 'UTF8';

copy reviews(rid, kid, rating, review)
            from 'C:\Users\Peter\Desktop\Durum\src\database\reviews.csv'
            delimiter ','
            CSV HEADER
            ENCODING 'UTF8';

