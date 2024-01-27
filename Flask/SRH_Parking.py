#Rohan Avale, Sagar Patil, Ghanashyam Ajayan

#SRH Parking 
#The parking spot 1 is the rear most spot in the parking lot 
#Vehicles can check in and check out randomly
#Vehicle Categories- Car,Bike,Truck (Prices-5,2,10 Euros respectively)
#Vehicle type and License Plate is taken as input
#The status of Parking lot is displayed- Total spots and available spots
#If Parking is full no more checkin is allowed
#The Price of the parking is adjusted to the state of filling
#The data is stored in a database using SQLite3
#The database can be deleted and created by itself without deleting the file 'parking.db'

#Sources-
#https://www.w3schools.com
#https://stackoverflow.com
#Suggestion for making database using SQLite3 from Prof. Lukasz Rojek

total = 375
chkin = 0

spot = [0] * 375  # availability of parking spot(0-available 1-occupied)

import sqlite3

conn = sqlite3.connect('parking.db')
c = conn.cursor()
c.execute('create table if not exists  parking(vehicle text,plate text,price real,spotnum integer)')
conn.commit()
c.execute("SELECT spotnum FROM parking")  # To get all the values in spotnum column https://www.w3schools.com/python/python_mysql_select.asphttps://www.w3schools.com/python/python_mysql_select.asp
conn.commit()
spots = c.fetchall()
print(spots)
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
        output = False
        exist = c.execute("select rowid from parking where spotnum = ? and plate=?",(no, plate)).fetchone()  # to check if both spotnum and plate match and are in one row
        # https://stackoverflow.com/questions/2440147/how-to-check-the-existence-of-a-row-in-sqlite-with-python
        if exist is None:
            print("The spot num and plate dont match")
        else:
            print("Yep exists")
            delete = """DELETE from parking where spotnum = ? and plate = ?"""
            c.execute(delete, (no, plate))  ##Delete the data while checkout if spotnum and plate match
            conn.commit()
            output = True

        c.execute("SELECT * FROM parking ")
        conn.commit()
        print(c.fetchall())
        conn.close()
        return output

    def checkin(self, spotnum):
        while True:
            # position in list
            print("1:Car \n2:Bike \n3:Truck")
            vtype = int(input("Enter vehicle type 1/2/3- "))

            if vtype == 1:
                vehicle = "Car"
                x = cost()
                price = 5 * x

            elif vtype == 2:
                vehicle = "Bike"
                x = cost()
                price = 2 * x

            elif vtype == 3:
                vehicle = "Truck"
                x = cost()
                price = 10 * x

            else:
                print("Checkin error")
                continue

            plate = input("Enter Plate Number- ")
            print("\n\n")
            print("Vehicle type: ", vehicle)
            print("Licence plate: ", plate)
            print("Parking Cost: ", price, " Euros")
            print("Your parking spot is", spotnum)
            datab = Park(spotnum) #Calling the class Park
            datab.database_in(vehicle, plate, price, spotnum) #call object in class

            spot[self.n] = 1  # 1 indicates that this spot is occupied
            print(spot)
            print("\n\n")
            break

    def checkout(self):
        while True:
            try:
                num = int(input("Enter Parking Spot Number- "))

                x = num - 1  # to search in list(spot)
                if spot[x] == 0:
                    print("This spot is empty Please enter correct spot number")
                    continue
                plate2 = input("Enter Plate Number- ")
                print("\n\n")
                databout = Park(num)
                out = databout.database_out(plate2, num)
                if out is True:
                    spot[x] = 0  # makes the spot available
                    print(spot)
                    print("Thank you.. Please Visit again\n\n")
                    break
                else:
                    continue


            except:
                print("Checkout error")


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


while True:
    try:
        print("Welcome to SRH Parking Lot\n")
        available = total - chkin
        print("Total: ", total, "  Available: ", available)
        check = int(input("Would you like to Check in or Check out? 1/2 \nPress 0 to end program\nPress 9 to delete and create new database\n"))
        if check == 1:
            if available > 0:
                spotnum = avail(spot)
                spotnum = spotnum + 1  # list starts from 0
                clspot = Park(spotnum) #calling the class Park
                clspot.checkin(spotnum)
                chkin = chkin + 1
            else:
                print(
                    "SORRY No Parking Available")  # If the parking garage is occupied, no further check-ins will be accepted.

        elif check == 2:
            if available == 375:
                print("The Parking Lot is empty")
                continue
            clsout = Park(spotnum)
            clsout.checkout()
            chkin = chkin - 1

        elif check == 0:
            break
        elif check == 9: # to delete the whole table in the database2212
            conn = sqlite3.connect('parking.db')
            c = conn.cursor()
            c.execute('drop table parking') #delete whole table
            conn.commit()
            spot = [0] * 375 #set list to 0
            chkin=0
            continue

        else:
            print("Please choose from 1,2,9 or 0")


    except:
        print("Wrong Input")
