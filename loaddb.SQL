CREATE TABLE IF NOT EXISTS kebabshop(
id integer PRIMARY KEY,
name varchar(100),
address text,
rating float(2),
x_coordinate float(7),
y_coordinate float(7),
tlfnr varchar(8));

copy  kebabshop(id, name, address, rating, x_coordinate, y_coordinate, tlfnr)
            from 'C:\Users\Peter\Desktop\Durum\src\database\durumsnedker.csv'
            delimiter ','
            CSV HEADER
            ENCODING 'UTF8';
