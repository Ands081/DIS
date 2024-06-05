from flask import Flask
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

db = "dbname='kebab' user='postgres' host='127.0.0.1' password = '123'"
conn = psycopg2.connect(db)

if __name__ == '__main__':
    app.run(debug=True)

