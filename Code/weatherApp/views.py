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
from flask import (
    render_template, Blueprint, request, jsonify, g
)
from . import (
    graphs,
    queries,
    weather, 
    db
)
from .auth import login_required

views_bp = Blueprint('views', __name__)

from datetime import datetime

@views_bp.route('/')
@login_required
def index():
    datb = db.get_db()
    user_id = g.user['userId']  # Assuming you have stored user data in the 'g' object

    # Fetch the user's city data from the database
    user_city_data = datb.execute(
        "SELECT * FROM City WHERE cityId = (SELECT cityId FROM User WHERE userId = ?)",
        (user_id,)
    ).fetchone()

    # Convert the specified date to the string format matching the database
    specified_date = datetime(2017, 3, 25).strftime('%Y-%m-%d')

    # Fetch the WeatherInstance data for the specified date (March 25, 2017)
    weather_data = datb.execute(
        "SELECT * FROM WeatherInstance WHERE cityId = ? AND date = ?",
        (user_city_data['cityId'], specified_date)
    ).fetchone()

    return render_template("index.html.jinja", user_city_data=user_city_data, weather_data=weather_data)


@views_bp.route('/weather_summary')
@login_required
def weather_summary():

    city_name = request.args.get('city_name')
    date = request.args.get('date')

    weather_dict = queries.get_weather_data(city_name, date)
    
    return render_template("weather_summary.html.jinja", weather_dict=weather_dict)

@views_bp.route('/map')
@login_required
def map():
    return render_template("map.html.jinja")

@views_bp.route('/graph')
def graph():
    figure_html = graphs.get_temp_figure_html()
    return render_template("graph.html.jinja", figure_html = figure_html)

@views_bp.route('/location_select')
@login_required
def location_select():
    return render_template("location_select.html.jinja")

#This page is used only to determine which weather icon to use on the map as a marker
@views_bp.route('/api/weather_icon')
def get_weather_icon():
    city_name = request.args.get('cityName')
    date = request.args.get('date')
    
    weather_dict = queries.get_weather_data(city_name, date)
    
    icon_name = weather.determine_icon_based_on_weather(weather_dict)
    
    return jsonify({'icon': icon_name})