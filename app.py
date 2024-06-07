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

@app.route('/', methods=["POST", "GET"])
def home():
    cur = conn.cursor()
    #Getting 10 random rows from Attributes
    tenrand = '''select * from Attributes order by random() limit 10;'''
    cur.execute(tenrand)
    punks = list(cur.fetchall())
    length = len(punks)

    #Getting random id from table Attributes 
    randint = '''select id from Attributes order by random() limit 1;'''
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

@app.route("/punks/<gender>/<types>/<skin>/<count>/<access>")
def querypage(gender, types, skin, count, access):
    cur = conn.cursor()
    rest = 0

    sqlcode = f'''select * from Attributes where '''
    if gender != "both":
        sqlcode += f''' gender = '{gender}' and'''
        rest += 1

    if types != "all":
        sqlcode += f''' type = '{types}' and'''
        rest += 1

    if skin != "all":
        sqlcode += f''' skin_tone = '{skin}' and'''
        rest += 1

    if access != "NaN":
        rest += 1
        sqlcode += f''' accessories ~* '{access}' and'''
    
    if int(count) != -1:
        rest += 1
        sqlcode += f''' count = '{count}' and'''

    if rest == 0: 
        sqlcode = f''' select * from Attributes'''

    else: 
        sqlcode  = sqlcode[:-3]

    cur.execute(sqlcode)
    ct = list(cur.fetchall())


    length = len(ct)

    return render_template("cryptoquery.html", content=ct, length=length)

@app.route("/punk/<punkid>", methods=["POST", "GET"])
def punkpage(punkid):
    cur = conn.cursor()
    """
    Instead of PunkID we would have our database content
    for 1 cryptopunk instead.
    """
    if not session.get('logged_in'):
        return render_template('login.html')

    if request.method == "POST":
        # Add til favourite
        username = session['username']
        try: 
            sql1 = f'''insert into favorites(id, username) values ('{punkid}', '{username}') '''
            cur.execute(sql1)
            conn.commit()
        except:
            conn.rollback()



    req = "https://cryptopunks.app/cryptopunks/details/"+ punkid
    response = requests.get(req)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select("table.ms-rteTable-default tr")
    pricelist = str(soup.find(class_="punk-history-row-bid")).split('\n')
    if len(pricelist) < 5:
        price = "10Ξ ($18,000)"
    else:
        price =pricelist[4].replace('</td>', '').replace('<td>','')

    sql1 = f''' select * from attributes where id = '{punkid}' '''

    cur.execute(sql1)

    ct = cur.fetchone()

    return render_template("cryptopunk.html", content=ct, price=price)

if __name__ == '__main__':
    app.run(debug=True)


