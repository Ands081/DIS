CREATE TABLE IF NOT EXISTS kebabshop(
kid integer PRIMARY KEY,
name varchar(100),
address text,
rating float(2),
x_coordinate float(7),
y_coordinate float(7),
tlfnr text);

CREATE TABLE IF NOT EXISTS reviews(
rid integer PRIMARY KEY,
kid integer,
rating float(2),
review text);

CREATE TABLE IF NOT EXISTS distance(
did integer PRIMARY KEY,
dist integer,
kid integer);

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

