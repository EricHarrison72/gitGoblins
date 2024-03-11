# ------------------------------------------------------
# views.py
'''
Contains all current view methods, which do some logic and
then call render_template().
- hello_world(): home page
- weather_summary(): basic weather summary (not dynamic)
'''
'''
TODO:
Create different blueprints for different parts of the app.
Each should be "registered" in a separate .py file, which 
contains the view methods associated with it. (right now
we only have one blueprint called 'bp', registered in this
file, and all our view methods use it.)
'''
'''
Start Code sources:
- [Flask docs tutorial - Application Setup](https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/)
'''
# ------------------------------------------------------
from flask import render_template, Blueprint, request
from . import db

bp = Blueprint('bp', __name__)

@bp.route('/')
def index():
    message = "THIS IS THE HOME PAGE. HI!"
    return render_template("index.html", message=message)

@bp.route('/weather_summary')
def weather_summary():
    datb = db.get_db()

    city_name = request.args.get('city_name')
    date = request.args.get('date')


    #SQL query to get data for specific city
    weather_data = datb.execute('''
        SELECT City.cityName, WeatherInstance.date, WeatherInstance.tempMax AS temp_high, 
               WeatherInstance.tempMin AS temp_low, WeatherInstance.rainfall, 
               rainToday AS raining, WeatherInstance.windGustSpeed AS wind_speed, 
               WeatherInstance.windGustDir AS wind_dir
        FROM WeatherInstance
        JOIN City ON WeatherInstance.cityId = City.cityId
        WHERE City.cityName = ? AND WeatherInstance.date = ?

    ''', (city_name,date,)).fetchone()
    

    if weather_data is None:
        # Handle the case where no weather data is found
        weather_list = ["No data", "N/A", 0, 0, 0.0, False, 0, "N/A"]
    else:
        weather_list = [
            weather_data['cityName'], 
            weather_data['date'], 
            weather_data['temp_high'], 
            weather_data['temp_low'], 
            weather_data['rainfall'], 
            weather_data['raining'], 
            weather_data['wind_speed'], 
            weather_data['wind_dir']
        ]
    
    return render_template("weather_summary.html", weather_list=weather_list)
#Login page
@bp.route('/login')
def login():
    
    return render_template("login.html")

#Sign up page
@bp.route('/register')
def register():
    
    return render_template("register.html")

@bp.route('/map')
def map():
    return render_template("map.html")