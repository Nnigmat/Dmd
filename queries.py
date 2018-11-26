from flask import Flask, render_template, request
from create_table import *
from generate_table import *
import sqlite3

create_table()
generate_table()

app = Flask(__name__)
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/q1', methods=('GET', 'POST'))
def q1(): # date is string in format "dd.mm.yyyy"
    if request.method == 'POST':
        query = "SELECT c.id FROM Car_orders co, Customers cust, Cars c WHERE cust.name = " + cust_name + " and strftime("%Y", co.date) = " + cur_date[2] + " and strftime("%m",co.date) = " + cur_date[1] + " and day(co.date) =" + cur_date[0] + " and c.color = 'red' and c.id like 'AN%'"
        cust_name = request.form['cur_name']
        cur_date = request.form['cur_date']
        cur_date = cur_date.split(".")

        c.execute(query)

        return c.fetchall()
    else:
        return render_template('q1.html')

@app.route('/q2', methods=('GET', 'POST'))
def q2():
    if request.method == 'POST':
        cur_date = request.form['cur_date']
        cur_date = cur_date.split(".")
        usage = []
        for i in range (0, 24):
            c.execute("SELECT COUNT(*) FROM Charge_orders WHERE day(date) = year(date) = " + cur_date[2] + " and strftime("%m",date) = " + cur_date[1] + " and strftime("%d", date) = " + cur_date[0] + " and strftime('%H', date) = " + str(i))
            usage.append(c.fetchone())
        output = ""
        for i in range (0, 24):
            output += str(i) + "h-" + str(i + 1) + "h:" + str(usage[i]) + "\n"
        return output
    else:
        return render_template('q2.html')

@app.route('/q3')
def q3():
    c.execute("SELECT COUNT(*) FROM Car_orders WHERE strftime('%H', date) >= 7 and strftime('%H', date) <= 10")
    morning = c.fetchone()
    c.execute("SELECT COUNT(*) FROM Car_orders WHERE strftime('%H', date) >= 12 and strftime('%H', date) <= 14")
    afternoon = c.fetchone()
    c.execute("SELECT COUNT(*) FROM Car_orders WHERE strftime('%H', date) >= 17 and strftime('%H', date) <= 19")
    evening = c.fetchone()

    output = "Morning: " + str(morning) + "\n Afternoon: " + str(afternoon) + "\n Evening: " + str(evening)
    return output

@app.route('/q4', methods=('GET', 'POST'))
def q4():
    if request.method == 'POST':
        cust_id = request.form['cust_id']
        cur_month = request.form['cur_month']
        c.execute("SELECT * FROM Car_orders WHERE customer_id = " + str(cust_id) + " and strftime("%m",date) = " + str(cur_month))
        return c.fetchall()

@app.route('/q5')
def q5():
    c.execute("SELECT AVG(distance) FROM Car_orders")
    output = c.fetchone() + "\n"
    c.execute("SELECT AVG(driving_time) FROM Car_orders")
    output += c.fetchone()
    return output

@app.route('/q6')
def q6():
    c.execute("SELECT TOP 3 starting_location, destination, COUNT(*) FROM Car_orders WHERE strftime('%H', date) >= 7 and strftime('%H', date) <= 10 GROUP BY starting_location, destination ORDER BY 3 DESC")
    morning = c.fetchone()
    c.execute("SELECT TOP 3 starting_location, destination, COUNT(*) FROM Car_orders WHERE strftime('%H', date) >= 12 and strftime('%H', date) <= 14 GROUP BY starting_location, destination ORDER BY 3 DESC")
    afternoon = c.fetchone()
    c.execute("SELECT TOP 3 starting_location, destination, COUNT(*) FROM Car_orders WHERE strftime('%H', date) >= 17 and strftime('%H', date) <= 19 GROUP BY starting_location, destination ORDER BY 3 DESC")
    evening = c.fetchone()

    output = "Morning: " + str(morning) + "\n Afternoon: " + str(afternoon) + "\n Evening: " + str(evening)
    return output

@app.route('/q7')
def q7():
    c.execute("SELECT COUNT(*) FROM Cars")
    cars_count = c.fetchall()[0][0]
    cars_drop = int(cars_count * 0.1)
    c.execute("SELECT co.car_id COUNT(*) FROM (Car_orders co, Cars c) WHERE co.car_id = c.id GROUP BY c.id ORDER BY 2 DESC LIMIT " + str(cars_drop))
    output = c.fetchall()
    return output

@app.route('/q8', methods=('GET', 'POST'))
def q8(cur_date):
    if request.method == 'POST':
        cur_date = request.form['cur_date']
        c.execute("SELECT customer_id, COUNT(*) FROM Charge_orders WHERE date >= " + str(cur_date))
        return c.fetchall()
    else:
        return render_template('q8.html')

@app.route('/q9')
def q9():
    c.execute("SELECT workshop_id, part_id, COUNT(*) FROM Parts_order GROUP BY workshop_id ORDER BY 3 DESC")
    output = [c.fetchone()]
    cur = output[0]
    while cur != (None, None, None):
        cur = c.fetchone()
        if output[len(output) - 1][len(output[0])] != cur[0]:
            output.append(cur)
    return cur

@app.route('/q10')
def q10():
    c.execute("SELECT c.id, AVG(ro.cost + co.cost) FROM Cars c, Repair_orders ro, Charge_orders co WHERE ro.car_id = c.id and co.car_id = c.id ORDER BY 2 DESC")
    return c.fetchall()
