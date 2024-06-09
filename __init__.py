from flask import Flask, render_template, redirect, url_for, session, abort, request, flash
from math import sin, cos, sqrt, atan2, radians
import geopy.distance
import requests
from bs4 import BeautifulSoup
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import glob
import pandas as pd
import random
import re

app = Flask(__name__)

db = "dbname='kebab' user='postgres' host='localhost' password = '123'"
conn = psycopg2.connect(db)

def tlftransform(tlfnr):
    pattern = re.compile(r'\[(\d{2})(\d{2})(\d{2})(\d{2})\]')
    transformed = re.sub(pattern, r'[\1 \2 \3 \4]', tlfnr)
    return transformed

@app.route('/', methods = ['GET','POST'])
def home():
    cur = conn.cursor()
    #10 random kebabshops
    rand_ten = '''select * from kebabshop order by random() limit 10;'''
    cur.execute(rand_ten)
    kebab = list(cur.fetchall())
    if request.method == 'POST':
        lat1 = float(request.form['latitude'])
        lon1 = float(request.form['longitude'])
        cur.execute(f'''SELECT x_coordinate, y_coordinate FROM kebabshop''')
        temp = cur.fetchall()
        for i in range(1, 50):
            lat2 = temp[i-1][0]
            lon2 = temp[i-1][1]
            c1 = (lat1, lon1)
            c2 = (lat2, lon2)
            tempdist = geopy.distance.distance(c1, c2).km
            cur.execute(f'''INSERT INTO distance (kid, dist) VALUES ('{i}', '{tempdist}') 
                            ON CONFLICT (kid) DO UPDATE SET dist ='{tempdist}' ''') 
            conn.commit()
    return render_template("index.html", content = kebab)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/shoplist")
def shoplist():
    cur = conn.cursor()
    allks = '''select * from kebabshop NATURAL JOIN distance'''
    cur.execute(allks)
    kebab = list(cur.fetchall())
    return render_template("shoplist.html", content = kebab)

@app.route("/<kid>")
def kebabshop(kid):
    cur = conn.cursor()
    sql1 = f''' select * from kebabshop where kid = '{kid}' '''
    cur.execute(sql1)
    c1 = cur.fetchone()

    sql2 = f''' select * from reviews where kid = '{kid}' '''
    cur.execute(sql2)
    c2 = cur.fetchall()
    return render_template("review.html", content = c1, rev = c2)


