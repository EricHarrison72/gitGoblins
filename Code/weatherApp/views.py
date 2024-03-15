# ------------------------------------------------------
# views.py
'''
Contains all current view methods, which do some logic and
then call render_template().
- hello_world(): home page
- weather_summary(): basic weather summary (not dynamic)
'''
'''
Start Code sources:
- [Flask docs tutorial - Application Setup](https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/)
'''
# ------------------------------------------------------
from flask import render_template, Blueprint, request, jsonify
from . import db
from .auth import login_required

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
#@login_required
def index():
    return render_template("index.html.jinja")

@views_bp.route('/weather_summary')
#@login_required
def weather_summary():

    city_name = request.args.get('city_name')
    date = request.args.get('date')

    weather_dict = queries.get_weather_data(city_name, date)
    
    return render_template("weather_summary.html.jinja", weather_dict=weather_dict)

@views_bp.route('/map')
#@login_required
def map():
    return render_template("map.html.jinja")

#This page is used only to determine which weather icon to use on the map as a marker
@views_bp.route('/api/weather_icon')
def get_weather_icon():
    city_name = request.args.get('cityName')
    date = request.args.get('date')
    
    # Use the database connection to query weather data
    db = db.get_db()
    weather_data = db.execute('''
        SELECT * FROM WeatherInstance
        JOIN City ON WeatherInstance.cityId = City.cityId
        WHERE City.cityName = ? AND WeatherInstance.date = ?
    ''', (city_name, date)).fetchone()
    
    # Assuming `determine_icon_based_on_weather` is a function that takes weather data and returns an icon name
    if weather_data:
        icon_name = determine_icon_based_on_weather(weather_data)
    else:
        icon_name = "default_icon"  # Fallback icon if no weather data found
    
    return jsonify({'icon': icon_name})