from flask import Flask
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

db = "dbname='kebab' user='postgres' host='localhost' password = '123'"
conn = psycopg2.connect(db)

@app.route("/")
def home():
    return 'Velkommen til min Flask-app!'

if __name__ == '__main__':
    app.run(debug=True)

