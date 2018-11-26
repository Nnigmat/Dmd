from flask import Flask, render_template, request
from create_table import *
from generate_table import *
import sqlite3

create_table()
generate_table()

app = Flask(__name__)
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

username = 'SalaJenyaNigma'
fullname = 'SalaJenyaNigma DinNigMak'
email = 'salajenyanigma@mail.ru'
location = '60,50'
phone = '9178764408'

c.execute('insert into Customers values(?, ?, ?, ?, ?, ?)', (None, username, fullname, email, location, phone))
c.execute('insert into Car_orders values(?, ?, ?, ?, ?, ?, ?, ?)', (None, str(n+1), '1', '50,60', '60,70', '100', '2018-01-01 17:30:30', '100'))
c.execute('insert into Car_orders values(?, ?, ?, ?, ?, ?, ?, ?)', (None, str(n+1), '1', '50,60', '60,70', '100', '2018-11-20 17:30:30', '100'))
c.execute('update Cars set plate="AN3333" where id=1')
c.execute('insert into Charge_orders values(?, ?, ?, ?, ?, ?, ?)', (None, '1', '20', '20', '1', '2018-01-01 17:30:30', str(n+1)))
conn.commit()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/q1', methods=('GET', 'POST'))
def q1(): # date is string in format "dd.mm.yyyy"
    if request.method == 'POST':
        cust_name = request.form['cur_name']
        cur_date = request.form['cur_date']
        dd, mm, yyyy = cur_date.split(".")
        query = 'SELECT c.id FROM Car_orders co, Customers cust, Cars c WHERE cust.username = "{}" and strftime("%Y", co.date) = "{}" and strftime("%m", co.date) = "{}" and strftime("%d", co.date)="{}" and c.color="red" and c.plate like "AN%"'.format(cust_name, yyyy, mm, dd)
        #query = 'SELECT c.id FROM Car_orders co, Customers cust, Cars c WHERE cust.username = "' + cust_name + '" and strftime("%Y", co.date) = "' + cur_date[2] + '" and strftime("%m",co.date) = "' + cur_date[1] + '" and strftime("%d", co.date) = "' + cur_date[0] + '" and c.color = "red" and c.id like "AN%"'
        c.execute(query)
        return str([el[0] for el in set(c.fetchall())])
    else:
        return render_template('q1.html')

@app.route('/q2', methods=('GET', 'POST'))
def q2():
    if request.method == 'POST':
        cur_date = request.form['cur_date']
        dd, mm, yyyy = cur_date.split(".")
        usage = []
        for i in range (0, 24):
            c.execute('select count(*) from Charge_orders where strftime("%Y", date)="{}" and strftime("%m", date)="{}" and strftime("%d", date)="{}" and strftime("%H", date)="{}"'.
                    format(yyyy, mm, dd, i))
            usage.append(c.fetchall()[0])
        output = ""
        for i in range (0, 24):
            output += str(i) + "h-" + str(i + 1) + "h:" + str(usage[i][0]) + "\n"

        return output
    else:
        return render_template('q2.html')

@app.route('/q3')
def q3():
    c.execute('SELECT COUNT(*) FROM Car_orders WHERE  date BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") and strftime("%H", date) between  strftime("%H", "2000-11-01 07:00:00") and strftime("%H", "2000-11-01 10:00:00")')
    morning = c.fetchone()
    c.execute('SELECT COUNT(*) FROM Car_orders WHERE date BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") and strftime("%H", date) between  strftime("%H", "2000-11-01 12:00:00") and strftime("%H", "2000-11-01 14:00:00")')
    afternoon = c.fetchone()
    c.execute('SELECT COUNT(*) FROM Car_orders WHERE date BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") and strftime("%H", date) between  strftime("%H", "2000-11-01 17:00:00") and strftime("%H", "2000-11-01 19:00:00")')
    evening = c.fetchone()

    output = "Morning: " + str(morning) + "\n Afternoon: " + str(afternoon) + "\n Evening: " + str(evening)
    return output

@app.route('/q4', methods=('GET', 'POST'))
def q4():
    if request.method == 'POST':
        cust_id = request.form['cust_id']
        cur_month = request.form['cur_month']
        c.execute('select * from Car_orders where customer_id="{}" and date between datetime("now", "-30 days") and datetime("now", "localtime")'.format(cust_id))
        return str(c.fetchall())
    else:
        return render_template("q4.html")


@app.route('/q5')
def q5():
    c.execute("SELECT AVG(distance) FROM Car_orders")
    output = str(c.fetchone()) + "\n"
    c.execute("SELECT AVG(driving_time) FROM Car_orders")
    output += str(c.fetchone())
    return output

@app.route('/q6')
def q6():
    c.execute('SELECT starting_location, destination, COUNT(*) FROM Car_orders WHERE strftime("%H", date) between  strftime("%H", "2000-11-01 07:00:00") and strftime("%H", "2000-11-01 10:00:00") GROUP BY starting_location, destination ORDER BY 3 DESC LIMIT 3')
    morning = c.fetchone()
    c.execute('SELECT starting_location, destination,COUNT(*) FROM Car_orders WHERE strftime("%H", date) between  strftime("%H", "2000-11-01 12:00:00") and strftime("%H", "2000-11-01 14:00:00") GROUP BY starting_location, destination ORDER BY 3 DESC LIMIT 3')
    afternoon = c.fetchone()
    c.execute('SELECT starting_location, destination,COUNT(*) FROM Car_orders WHERE strftime("%H", date) between  strftime("%H", "2000-11-01 17:00:00") and strftime("%H", "2000-11-01 19:00:00") GROUP BY starting_location, destination ORDER BY 3 DESC LIMIT 3')
    evening = c.fetchone()

    output = "Morning: " + str(morning) + "\n Afternoon: " + str(afternoon) + "\n Evening: " + str(evening)
    return output

@app.route('/q7')
def q7():
    c.execute("SELECT COUNT(*) FROM Cars")
    cars_count = c.fetchall()[0][0]
    cars_drop = int(cars_count * 0.1)
    c.execute("SELECT co.car_id COUNT(*) FROM Car_orders co, Cars c WHERE co.car_id = c.id GROUP BY c.id ORDER BY 2 DESC LIMIT " + str(cars_drop))
    output = c.fetchall()
    return output

@app.route('/q8', methods=('GET', 'POST'))
def q8(cur_date=1):
    if request.method == 'POST':
        cur_date = request.form['cur_date']
        c.execute("SELECT customer_id, COUNT(*) FROM Charge_orders WHERE date >= \'" + str(cur_date) + "\'")
        return c.fetchall()
    else:
        return render_template('q8.html')

@app.route('/q9')
def q9():
    c.execute("SELECT workshop_id, part_id, COUNT(*) FROM Parts_orders GROUP BY workshop_id ORDER BY 3 DESC")
    output = [c.fetchone()]
    cur = ""
    cur += str(output[0])
    while cur != (None, None, None) or cur != None:
        cur = c.fetchone()
        if cur == None:
            break;
        if output[len(output) - 1][len(output[0]) - 1] != cur[0]:
            output.append(cur)
    print(output)
    return str(output)

@app.route('/q10')
def q10():
    c.execute("SELECT c.id, AVG(ro.cost + co.price) FROM Cars c, Repair_orders ro, Charge_orders co WHERE ro.car_id = c.id and co.car_id = c.id ORDER BY 2 DESC")
    return str(c.fetchall())
