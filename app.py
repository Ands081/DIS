from flask import Flask, render_template, redirect, url_for, session, abort, request, flash
import requests
from bs4 import BeautifulSoup
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import glob
import pandas as pd
import random

app = Flask(__name__)

db = "dbname='kebab' user='postgres' host='localhost' password = '123'"
conn = psycopg2.connect(db)
cursor = conn.cursor()

@app.route('/', methods=["POST", "GET"])
def home():
    cur = conn.cursor()
    #Getting 10 random rows from Attributes
    tenrand = '''select * from kebabshop order by random() limit 10;'''
    cur.execute(tenrand)
    punks = list(cur.fetchall())
    length = len(punks)

    #Getting random id from table Attributes 
    randint = '''select id from kebabshop order by random() limit 1;'''
    cur.execute(randint)
    randomNumber = cur.fetchone()[0]
    if request.method == "POST":
        input_gender = request.form["radio"].lower()
        input_type = request.form["radiotype"].lower()
        input_skin = request.form["radioskin"].lower()

        input_count = request.form["accessCount"] or -1
        input_access = request.form["access"].lower() or "NaN"

        input_id = request.form["punkid"].lower() or ""

        if input_id != "":
            input_id = input_id.zfill(4)
            return redirect(url_for("punkpage", punkid=input_id))
        return redirect(url_for("querypage", gender=input_gender, types=input_type, skin=input_skin, access=input_access, count=input_count))
            
    length = len(punks)
    return render_template("index.html", content=punks, length=length, randomNumber = randomNumber)

@app.route("/kontakt")
def contact():
    return render_template("kontakt.html")

@app.route("/listen")
def listen():
    cur = conn.cursor()
    tenrand = '''select * from kebabshop'''
    cur.execute(tenrand)
    punks = list(cur.fetchall())
    return render_template("listen.html", content=punks)

@app.route("/<punkid>", methods=["POST", "GET"])
def punkpage(punkid):
    cur = conn.cursor()
    sql1 = f''' select * from attributes where id = '{punkid}' '''

    cur.execute(sql1)

    ct = cur.fetchone()

    return render_template("cryptopunk.html", content=ct)

if __name__ == '__main__':
    app.run(debug=True)


