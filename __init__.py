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

    return render_template("index.html", content = kebab)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/shoplist")
def shoplist():
    cur = conn.cursor()
    allks = '''select * from kebabshop'''
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


