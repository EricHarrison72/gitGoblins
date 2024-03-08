# ------------------------------------------------------
# db.py
'''
Methods for creating, accessing and tearing down the 
database using the specs in schema.sql.
'''
'''
Starter code source:
- [Flask docs tutorial - Define and Access the Database](https://flask.palletsprojects.com/en/3.0.x/tutorial/database/)
'''
# ------------------------------------------------------
import sqlite3
import click
import csv
import os
from flask import current_app, g
from flask.cli import with_appcontext

city_to_id = {} # var used to populate db
weather_data_file = os.path.join("data", "weatherAUS.csv")

#Returns current database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

#Closes current database
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#Initializes database to app using schema.sql
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    populate_db()

#---------------------------
# DATABASE POPULATION

# populates the db with data from weatherAUS.csv     
def populate_db():
    # Database connection
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cur = conn.cursor()

    # Read from the CSV into the database
    with open(weather_data_file, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)  # Skip the header row
        
        #Read the values of each row in the csv into the database
        for row in csvreader:
            city = location_to_id(row[1], cur) 
            date, min_temp, max_temp, sunshine, rainfall = row[0], row[2], row[3], row[6], row[4]
            evaporation, cloud9am, cloud3pm, pressure9am, pressure3pm = row[5], row[17], row[18], row[15], row[16]
            humidity9am, humidity3pm, wind_gust_speed, wind_gust_dir = row[13], row[14], row[8], row[7]
            wind_speed_9am, wind_speed_3pm, wind_dir_9am, wind_dir_3pm = row[11], row[12], row[9], row[10]
            rain_today, rain_tomorrow = row[21], row[22]
            
            # Prepare INSERT statement for WeatherInstance
            insert_sql = '''INSERT INTO WeatherInstance (cityId, date, tempMin, tempMax, sunshine, rainfall, evaporation, cloud9am, cloud3pm, pressure9am, pressure3pm, humidity9am, humidity3pm, windGustSpeed, windGustDir, windSpeed9am, windSpeed3pm, windDir9am, windDir3pm, rainToday, rainTomorrow)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

            cur.execute(insert_sql, (city, date, min_temp, max_temp, sunshine, rainfall, evaporation, cloud9am, cloud3pm, pressure9am, pressure3pm, humidity9am, humidity3pm, wind_gust_speed, wind_gust_dir, wind_speed_9am, wind_speed_3pm, wind_dir_9am, wind_dir_3pm, rain_today, rain_tomorrow))
    
    conn.commit()
    conn.close()

# (Helper method) Returns cityId for specified city name from dictionary
def location_to_id(city, cur):
    global city_to_id  # Add this line to use the module-level city_to_id
    if len(city_to_id) == 0: #If city_to_id is empty, initialize it
        city_to_id = initialize_cities(cur)
    return city_to_id[city]
    
# (Helper method) Initialize dictionary for city_to_cityId
#Also read city values into city table in SQL schema, since we can only do this once per city it goes here
def initialize_cities(cur):
    i=0
    rows = []
    cities = {}
    
    #Read csv row by row, if the city doesn't exist in the dictionary, add it with corresponding id i
    with open(weather_data_file, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader) #Skip header
        for row in csvreader:
            rows.append(row)
            #If the city is new to the dictionary, add to dictionary and to SQL schema
            if row[1] not in cities:
                cities[row[1]]=i
                
                # Prepare INSERT statement for City
                insert_sql = '''INSERT INTO City (cityId, cityName)
                                VALUES (?, ?)'''
                cur.execute(insert_sql, (i, row[1],))
                
                i+=1
    
    return cities

#-------------------------------

#Used for initializing database via command line, I couldn't make it work properly - Eric
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

#Used to initialized database commands
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
