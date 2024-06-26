from flask import Flask, render_template, request
import geopy.distance
import psycopg2
import re

app = Flask(__name__)

db = "dbname='kebab' user='postgres' host='localhost' password = '123'"
conn = psycopg2.connect(db)

def distformat(distance):
    # Regular expression to match numbers with more than 2 decimal places
    pattern = re.compile(r'\d+.\d{3,}')

    # Replace matched numbers with numbers rounded to 2 decimal places and add 'km'
    distformat = re.sub(pattern, lambda x: f'{float(x.group()):.2f} km', distance)
    return distformat

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
        for i in range(1, 51):
            lat2 = temp[i-1][0]
            lon2 = temp[i-1][1]
            c1 = (lat1, lon1)
            c2 = (lat2, lon2)
            tempdist = distformat(str(geopy.distance.distance(c1, c2).km))
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
    allks = '''select * from kebabshop FULL JOIN distance ON kebabshop.kid = distance.kid'''
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


