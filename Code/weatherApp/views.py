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
    render_template, Blueprint, request, jsonify
)
from . import (
    graphs,
    queries,
    weather,
    predictions
)
from .auth import login_required

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
@login_required
def index():
    return render_template("index.html.jinja")

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

#This page is used only to run predictions code while creating the model
@views_bp.route('/api/predict_weather')
def predict_weather():
    df = predictions.create_dataframe()
    df = predictions.process_data(df)
    predictions.build_model(df)
    
    return render_template("index.html.jinja")