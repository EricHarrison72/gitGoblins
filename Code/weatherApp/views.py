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
from . import db, queries
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

@views_bp.route('/location_select')
#@login_required
def location_select():
    return render_template("location_select.html.jinja")

#This page is used only to determine which weather icon to use on the map as a marker
@views_bp.route('/api/weather_icon')
def get_weather_icon():
    city_name = request.args.get('cityName')
    date = request.args.get('date')
    
    weather_dict = queries.get_weather_data(city_name, date)
    
    if weather_dict is not None:
        icon_name = determine_icon_based_on_weather(weather_dict)
    else:
        icon_name = 'error'  # Fallback icon if no weather data found
    
    return jsonify({'icon': icon_name})

def determine_icon_based_on_weather(weather_data):
    # Helper function to safely convert to int, handling 'NA', 'N/A', etc.
    def safe_int(value, default=0):
        try:
            return int(value)
        except ValueError:
            return default

    #If high and low temps are 0 it means there was no data for that day
    if (weather_data['temp_high'] == 0) & (weather_data['temp_low'] == 0):
        return 'error'
    
    if weather_data['raining'] == "Yes":
        return 'rain'

    wind_speed = safe_int(weather_data['wind_speed'])
    if wind_speed > 80:
        return 'wind'

    cloud_cover = safe_int(weather_data['cloud'])
    if cloud_cover > 4:
        return 'cloud'
    elif cloud_cover > 0:
        return 'partcloud'

    return 'sun'
