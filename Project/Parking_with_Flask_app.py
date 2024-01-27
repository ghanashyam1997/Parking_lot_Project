# Rohan Avale, Sagar Patil, Ghanashyam Ajayan
# SRH PARKING WEBSITE
# python -m flask run (to run flask in terminal)
# Sources-
# https://www.w3schools.com
# https://stackoverflow.com
# https://getbootstrap.com


from flask import Flask,redirect
from flask import render_template
from flask import request
from flask.helpers import url_for

app = Flask(__name__)

total = 375
chkin = 0

spot = [0] * 375  # availability of parking spot(0-available 1-occupied)

import sqlite3

conn = sqlite3.connect('parking.db')
c = conn.cursor()
c.execute('create table if not exists  parking(vehicle text,plate text,price real,spotnum integer)')
conn.commit()
c.execute(
    "SELECT spotnum FROM parking")  # To get all the values in spotnum column https://www.w3schools.com/python/python_mysql_select.asphttps://www.w3schools.com/python/python_mysql_select.asp
conn.commit()
spots = c.fetchall()
# print(spots)
q = 0
for i in spots:  # take all the values under spotnum column and put 1 in their respective index in spot list as occupied
    a = spots[q][0]
    # print(a)
    a = a - 1  # to set index in list spot
    spot[a] = 1  # 1 means occupied
    q = q + 1
    chkin = chkin + 1
conn.close


class Park:
    def __init__(self, spotnum):
        self.n = spotnum - 1

    def database_in(self, v, p, d, s):  # during checkin all the data is saved in database
        conn = sqlite3.connect('parking.db')
        c = conn.cursor()
        c.execute('create table if not exists  parking(vehicle text,plate text,price real,spotnum integer)')
        c.execute("insert into parking values (?,?,?,?)", (v, p, d, s))  ##variables
        conn.commit()
        c.execute("SELECT * FROM parking ")
        conn.commit()
        print(c.fetchall())
        conn.close()

    def database_out(self, plate, no):  # during checkout the data is deleted from the database
        conn = sqlite3.connect('parking.db')
        c = conn.cursor()
        out1 = False
        exist = c.execute("select rowid from parking where spotnum = ? and plate=?",
                          (no, plate)).fetchone()  # to check if both spotnum and plate match and are in one row
        # https://stackoverflow.com/questions/2440147/how-to-check-the-existence-of-a-row-in-sqlite-with-python
        if exist is None:
            print("The spot num and plate dont match")
            return out1
        else:
            print("Yep exists")
            delete = """DELETE from parking where spotnum = ? and plate = ?"""
            c.execute(delete, (no, plate))  ##Delete the data while checkout if spotnum and plate match
            conn.commit()
            out1 = True

        c.execute("SELECT * FROM parking ")
        conn.commit()
        print(c.fetchall())
        conn.close()
        return out1

    def checkin(self, spotnum, vtype, plate):
        if vtype == '1':
            vehicle = "Car"
            x = cost()
            price = 5 * x

        elif vtype == '2':
            vehicle = "Bike"
            x = cost()
            price = 2 * x

        elif vtype == '3':
            vehicle = "Truck"
            x = cost()
            price = 10 * x

        datab = Park(spotnum)  # Calling the class Park
        datab.database_in(vehicle, plate, price, spotnum)  # call function in class
        spot[self.n] = 1  # 1 indicates that this spot is occupied
        print(spot)
        return vehicle, price

    def checkout(self, plate2, spotnum):

        if spot[self.n] == 0:
            print("This spot is empty Please enter correct spot number")
        databout = Park(self.n)
        out2 = databout.database_out(plate2, spotnum)
        if out2 is True:
            spot[self.n] = 0  # makes the spot available
            print(spot)
        return out2


def avail(p):  # finds the first empty parking space
    for i in p:
        if i == 0:
            return spot.index(i)  # syntax from stackoverflow('i' is the value but we need the position)


def cost():  # The price for parking should be adjusted to the state of filling.
    if available >= 187:  # if availability is more than 50% then price is reduced by 50%
        p = 0.5
    if available < 187 & available >= (round(375 * 0.4)):  # for every 10% increase in occupancy 10% rise in price
        p = 0.6
    if available < (round(375 * 0.4)) & available >= (round(375 * 0.3)):
        p = 0.7
    if available < (round(375 * 0.3)) & available >= (round(375 * 0.2)):
        p = 0.8
    if available < (round(375 * 0.2)) & available >= (round(375 * 0.1)):
        p = 0.9
    if available < (round(375 * 0.1)):
        p = 1
    return p


available = total - chkin


# Home

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('Home.html')


# Checkin

@app.route("/Checkin", methods=['GET', 'POST'])
def Checkin():
    return render_template("Checkin.html")


@app.route("/Checkin_submit", methods=['GET', 'POST'])
def Checkin_submit():
    vetype = request.form.get(
        'vetype')  # https://stackoverflow.com/questions/32019733/getting-value-from-select-tag-using-flask
    plate = request.form.get('plate')
    chkin = total - available
    if available > 0:
        spotnum = avail(spot)
        spotnum = spotnum + 1  # list starts from 0
        clspot = Park(spotnum)  # calling the class Park
        vehicost = clspot.checkin(spotnum, vetype, plate)  # vehicost has vehicle type and price in form of list
        chkin = chkin + 1
        return render_template("Result_in.html", value1=vehicost[0], value2=plate, value3=vehicost[1],
                               value4=spotnum)  # Send values to display on website
        # https://stackoverflow.com/questions/45149420/pass-variable-from-python-flask-to-html-in-render-template/45151521


# Checkout


@app.route("/Checkout", methods=['GET', 'POST'])
def Checkout():
    return render_template('Checkout.html')


@app.route("/Checkout_submit", methods=['GET', 'POST'])
def Checkout_submit():
    spot = int(request.form.get('spot'))  # spot is a string so convert to integer
    plate = request.form.get('plate')
    clspot = Park(spot)  # calling the class Park
    out3 = clspot.checkout(plate, spot)  # Calling function in class
    if out3 is True:  # Spot and plate number match
        return render_template("Result_out.html")
    else:
        return render_template("Result_outerror.html")
