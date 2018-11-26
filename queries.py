from flask import Flask
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

@app.route('/q1')
def q1(cust_name, cur_date): # date is string in format "dd.mm.yyyy"
    cur_date = cur_date.split(".")
    query = "SELECT c.id FROM Car_orders co, Customers cust, Cars c WHERE cust.name = " + cust_name + " and year(co.date) = " + cur_date[2] + " and month(co.date) = " + cur_date[1] + " and day(co.date) =" + cur_date[0] + " and c.color = 'red' and c.id like 'AN%'"

    c.execute(query)

    return c.fetchall()

@app.route('/q2')
def q2(cur_date):
    cur_date = cur_date.split(".")
    usage = []
    for i in range (0, 24):
        c.execute("SELECT COUNT(*) FROM Charge_orders WHERE day(date) = year(date) = " + cur_date[2] + " and month(date) = " + cur_date[1] + " and day(date) = " + cur_date[0] + " and datepart(HOUR, date) = " + str(i))
        usage.append(c.fetchone())
    output = ""
    for i in range (0, 24):
        output += str(i) + "h-" + str(i + 1) + "h:" + str(usage[i]) + "\n"
    return output

@app.route('/q3')
def q3():
    c.execute("SELECT COUNT(*) FROM Car_orders WHERE datepart(HOUR, date) >= 7 and datepart(HOUR, date) <= 10")
    morning = c.fetchone()
    c.execute("SELECT COUNT(*) FROM Car_orders WHERE datepart(HOUR, date) >= 12 and datepart(HOUR, date) <= 14")
    afternoon = c.fetchone()
    c.execute("SELECT COUNT(*) FROM Car_orders WHERE datepart(HOUR, date) >= 17 and datepart(HOUR, date) <= 19")
    evening = c.fetchone()

    output = "Morning: " + str(morning) + "\n Afternoon: " + str(afternoon) + "\n Evening: " + str(evening)
    return output

@app.route('/q4')
def q4(cust_id, cur_month):
    c.execute("SELECT * FROM Car_orders WHERE customer_id = " + str(cust_id) + " and month(date) = " + str(cur_month))
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
    c.execute("SELECT TOP 3 starting_location, destination, COUNT(*) FROM Car_orders WHERE datepart(HOUR, date) >= 7 and datepart(HOUR, date) <= 10 GROUP BY starting_location, destination ORDER BY 3 DESC")
    morning = c.fetchone()
    c.execute("SELECT TOP 3 starting_location, destination, COUNT(*) FROM Car_orders WHERE datepart(HOUR, date) >= 12 and datepart(HOUR, date) <= 14 GROUP BY starting_location, destination ORDER BY 3 DESC")
    afternoon = c.fetchone()
    c.execute("SELECT TOP 3 starting_location, destination, COUNT(*) FROM Car_orders WHERE datepart(HOUR, date) >= 17 and datepart(HOUR, date) <= 19 GROUP BY starting_location, destination ORDER BY 3 DESC")
    evening = c.fetchone()

    output = "Morning: " + str(morning) + "\n Afternoon: " + str(afternoon) + "\n Evening: " + str(evening)
    return output

@app.route('/q7')
def q7():
    c.execute("SELECT TOP 10 PERCENT co.car_id COUNT(*) FROM (Car_orders co, Cars c) WHERE co.car_id = c.id GROUP BY c.id ORDER BY 2 DESC")
    output = c.fetchall()
    return output

@app.route('/q8')
def q8(cur_date):
    c.execute("SELECT customer_id, COUNT(*) FROM Charge_orders WHERE date >= " + str(cur_date))
    return c.fetchall()

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
