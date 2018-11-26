from sqlite3 import connect

def create_table():
    try:
        conn = connect('database.db')
    except:
        conn = open('database.db', 'w+')
        conn = connect('database.db')

    c = conn.cursor()

# Create Customers table
    c.execute('''
            create table if not exists Customers (
                id integer primary key,
                username varchar(30),
                full_name varchar(50),
                email varchar(30),
                location varchar(50),
                phone_number varchar(10)
            )
            ''')

# Create Models table
    c.execute('''
            create table if not exists Models (
                id integer primary key,
                name varchar(50)
            )
            ''')

# Create Cars table
    c.execute('''
            create table if not exists Cars (
                id integer primary key,
                location varchar(50),
                charge_amount integer,
                color varchar(50),
                model_id integer,

                foreign key (model_id) references Models(id)
            )
            ''')

# Create Charging_stations table
    c.execute('''
            create table if not exists Charging_stations (
                id integer primary key,
                location varchar(50),
                available_sockets integer,
                cost decimal,
                time_of_charging integer,
                size_of_plugs integer,
                shape_of_plugs varchar(50)
            )
            ''')

# Create Charge_orders table
    c.execute('''
            create table if not exists Charge_orders (
                id integer primary key,
                car_id integer,
                price integer,
                charging_time integer,
                charging_station_id integer,
                date datetime default current_timestamp,
                customer_id integer,

                foreign key (customer_id) references Customer(id),
                foreign key (car_id) references Cars(id),
                foreign key (charging_station_id) references Charging_stations(id)
            )
            ''')

# Create Car_orders table
    c.execute('''
            create table if not exists Car_orders (
                    id integer primary key,
                    customer_id integer,
                    car_id integer,
                    starting_location varchar(50),
                    destination varchar(50),
                    driving_time integer,
                    date datetime default current_timestamp,
                    distance decimal,

                    foreign key (car_id) references Cars(id),
                    foreign key (customer_id) references Customers(id)
            )
            ''')

    c.execute('''
            create table if not exists Parts (
                    id integer primary key,
                    name varchar(50),
                    type varchar(50)
            )
            ''')

    c.execute('''
            create table if not exists Supported_models (
                    id integer primary key,
                    part_id integer,
                    model_id integer,
                    foreign key (part_id) references Parts(id),
                    foreign key (model_id) references Models(id)
            )
            ''')

    c.execute('''
            create table if not exists Available_workshop_parts (
                    id integer primary key,
                    part_id integer,
                    workshop_id integer,
                    amount integer,

                    foreign key (part_id) references Parts(id),
                    foreign key (workshop_id) references Workshop(id)
            )
            ''')

    c.execute('''
            create table if not exists Workshops (
                    id integer primary key,
                    location varchar(50),
                    available_parts_id integer,
                    availability_of_timing integer,

                    foreign key (available_parts_id) references Available_workshop_parts(id)
            )
            ''')

    c.execute('''
            create table if not exists Repair_orders (
                    id integer primary key,
                    car_id integer,
                    customer_id integer,
                    date datetime default current_timestamp,
                    cost decimal,

                    foreign key (car_id) references Cars(id),
                    foreign key (customer_id) references Customers(id)
            )
            ''')

    c.execute('''
            create table if not exists Parts_orders (
                    id integer primary key,
                    workshop_id integer,
                    part_id integer,
                    part_distributor_id integer,
                    date datetime default current_timestamp,
                    cost decimal,

                    foreign key (workshop_id) references Workshops(id),
                    foreign key (part_id) references Parts(id),
                    foreign key (part_distributor_id) references Car_parts_distributors(id)
            )
            ''')

    c.execute('''
            create table if not exists Available_distributors_parts (
                    id integer primary key,
                    part_id integer,
                    amount integer,

                    foreign key (part_id) references Parts(id)
            )
            ''')

    c.execute('''
            create table if not exists Car_parts_distributors (
                    id integer key,
                    name varchar(50),
                    address varchar(50),
                    phone_number varchar(50),
                    available_parts_id integer,
                    foreign key (available_parts_id) references Available_distributors_parts(id)
            )
            ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
