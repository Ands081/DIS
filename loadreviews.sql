CREATE TABLE IF NOT EXISTS reviews(
id integer,
rating float(2),
review text);

copy  reviews(id, rating, review)
            from 'C:\Users\Peter\Desktop\Durum\src\database\reviews.csv'
            delimiter ','
            CSV HEADER
            ENCODING 'UTF8';