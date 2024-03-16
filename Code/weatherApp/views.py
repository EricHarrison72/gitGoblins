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
from flask import render_template, Blueprint, request
from . import queries
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

@views_bp.route('/graph')
def graph():
    return render_template("graph.html.jinja")