CREATE TABLE IF NOT EXISTS kebabshop(
id integer PRIMARY KEY,
name varchar(100),
address text,
rating float(2),
x_coordinate float(7),
y_coordinate float(7));

copy  kebabshop(id, name, address, rating, x_coordinate, y_coordinate)
            from 'C:\Users\Peter\Desktop\Durum\src\database\durumsnedker.csv'
            delimiter ','
            CSV HEADER;


