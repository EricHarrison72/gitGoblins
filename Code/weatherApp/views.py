#views.py
from flask import Flask, render_template, Blueprint, current_app
from . import db

bp = Blueprint('bp', __name__)

@bp.route('/')
def hello_world():
    message = "Hello World!"
    return render_template("index.html", message=message)

@bp.route('/weather_summary')
def weather_summary():
    datb = db.get_db()

    city_id = 0 #City set to 1, as there's no way of collecting specific city id from webpage yet
    date = "2008-12-01" #Date set to first row of data


    #SQL query to get data for specific city
    weather_data = datb.execute('''
        SELECT City.cityName, WeatherInstance.date, WeatherInstance.tempMax AS temp_high, 
               WeatherInstance.tempMin AS temp_low, WeatherInstance.rainfall, 
               rainToday AS raining, WeatherInstance.windGustSpeed AS wind_speed, 
               WeatherInstance.windGustDir AS wind_dir
        FROM WeatherInstance
        JOIN City ON WeatherInstance.cityId = City.cityId
        WHERE WeatherInstance.cityId = ? AND WeatherInstance.date = ?

    ''', (city_id,date,)).fetchone()
    

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
