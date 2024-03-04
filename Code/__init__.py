#__innit__.py
from flask import Flask, render_template

import os, csv, sqlite3

city_to_id = {}
app = Flask(__name__, instance_relative_config=True)

#Initalizes database and returns app with working db
def create_app():
    #This isn't supposed to be necessary, but the next line wasn't working properly
    app.config['DATABASE'] = '/instance/database.db' 
    
    # Load configuration from 'instance/config.py'
    app.config.from_pyfile('config.py', silent=False)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    
    
    # Import and register the database commands from db.py
    from . import db
    db.init_app(app)
    
    #I couldn't figure out blueprints, maybe they'll help once I figure them out -Eric
    # Import and register your blueprints
    #from .views import bp as app_blueprint
    #app.register_blueprint(app_blueprint)
    
    # Initialize the database
    with app.app_context():
        db.init_db()
    
    # Database connection
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()


    # Read from the CSV into the database
    with open("data\\weatherAUS.csv", 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)  # Skip the header row
        
        #Read the values of each row in the csv into the database
        for row in csvreader:
            city = location_to_id(row[1]) 
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
    
    return app

#Returns cityId for specified city name from dictionary
def location_to_id(city):
    global city_to_id  # Add this line to use the module-level city_to_id
    if len(city_to_id) == 0: #If city_to_id is empty, initialize it
        city_to_id = initialize_cities(city)
    return city_to_id[city]
    
#Initialize dictionary for city_to_cityId
#Also read city values into city table in SQL schema, since we can only do this once per city it goes here
def initialize_cities(city):
    # Database connection
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    
    i=0
    rows = []
    cities = {}
    
    #Read csv row by row, if the city doesn't exist in the dictionary, add it with corresponding id i
    with open("data\\weatherAUS.csv", 'r') as file:
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
                
    conn.commit()
    conn.close()
    
    return cities