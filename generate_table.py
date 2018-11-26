from sqlite3 import connect
import string, random

def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def loc_gen():
    return str(random.uniform(40, 60))+','+str(random.uniform(40, 60))


def rand_timestamp():
    return '2018-'+str(random.randint(1, 12))+'-'+\
           str(random.randint(1, 30))+' '+str(random.randint(0, 24))+':'+str(random.randint(0,60))+':'+str(random.randint(0,60))


def generate_table():
    try:
        conn = connect('database.db')
    except:
        conn = open('database.db', 'w+')
        conn = connect('database.db')

    c = conn.cursor()
    n = 10

    c.execute('''
            create table if not exists Models (
                id integer primaty key,
                name varchar(50)
            )
            ''')

    for i in range(n):
        #customers
        c.execute('insert into Customers values(?, ?, ?, ?, ?, ?)', (None, string_generator(8, chars=string.ascii_lowercase),
            string_generator(5, chars=string.ascii_lowercase) + ' ' +string_generator(8, chars=string.ascii_lowercase),
            string_generator(6, chars=string.ascii_lowercase)+'@mail.ru',
            loc_gen(), string_generator(10, chars=string.digits)))

        #models
        c.execute('insert into Models values(?, ?)', (None, string_generator(10, chars=string.ascii_lowercase)))

        #cars
        c.execute('insert into Cars values(?, ?, ?, ?, ?)', (None, loc_gen(),
                                                          string_generator(2, string.digits), random.randint(1, n), random.randint(1, n)))

        # charging stations
        c.execute('insert into Charging_stations values(?, ?, ?, ?, ?, ?, ?)', (None, loc_gen(), string_generator(2, chars=string.digits),
                                                                                string_generator(3, chars=string.digits), string_generator(5, chars=string.digits),
                                                                                string_generator(1, chars=string.digits), string_generator(1, chars=string.ascii_lowercase)))

        # Create Charge_orders table
        c.execute('insert into Charge_orders values(?,?,?,?,?,?)', (None, random.randint(1, n), random.randint(1, 100),
                                                                  random.randint(100, 1000), random.randint(1, n), rand_timestamp()))

        #Parts
        c.execute('insert into Parts values(?,?,?)', (None, string_generator(10, string.ascii_lowercase),
                                                      string_generator(10, string.ascii_lowercase)))


    for i in range(n):
        #Car_orders
        c.execute('insert into Car_orders values(?,?,?,?,?,?,?)', (None, random.randint(1, n), random.randint(1, n),
                                                                 loc_gen(), loc_gen(),
                                                                 random.randint(100, 10000), rand_timestamp()))

        #Supported_models
        c.execute('insert into Supported_models values(?,?,?)', (None, random.randint(1, n), random.randint(1, n)))

        #Available_workshop_parts
        c.execute('insert into Available_workshop_parts values(?, ?, ?, ?)', (None, random.randint(1, n), random.randint(1, n), random.randint(0, 100)))

        #Workshops
        c.execute('insert into Workshops values(?,?,?,?)', (None, loc_gen(), random.randint(1, n), random.randint(0, 10)))

        #Repair_orders
        c.execute('insert into Repair_orders values (?,?,?,?,?)', (None, random.randint(1, n), random.randint(1, n),
                                                                   rand_timestamp(), random.uniform(10, 100)))

        #Parts_orders
        c.execute('insert into Parts_orders values(?,?,?,?,?,?)', (None, random.randint(1, n), random.randint(1, n), random.randint(1, n),
                                                                   rand_timestamp(), random.uniform(10, 100)))

        #Available_distributors_parts
        c.execute('insert into Available_distributors_parts values(?,?,?)', (None, random.randint(1, n), random.randint(0, 100)))

        #Car_parts_distributors
        c.execute('insert into Car_parts_distributors values(?,?,?,?,?)', (None, string_generator(10, string.ascii_lowercase),
                                                                           loc_gen(), string_generator(10, string.digits),
                                                                           random.randint(0, n)))


    conn.commit()
    conn.close()
