# ------------------------------------------------------
# views.py
'''
Contains view methods for feature and home pages, which
route URLs to the correct HTML template (and maybe do a 
little logic in between).
'''
'''
Start Code sources:
- [Flask docs tutorial - Application Setup](https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/)
'''
# ------------------------------------------------------
from flask import (
    redirect,
    render_template,
    Blueprint,
    request,
    jsonify,
    g,
    url_for
)
from . import (
    graphs,
    queries,
    weather,
    predictions,
    db,
)
from .auth import login_required
from datetime import datetime

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
@login_required
def index():
    user_id = g.user['userId']
    city_name = queries.get_user_city(user_id)
    specified_date = datetime(2017, 6, 24).strftime('%Y-%m-%d')

    weather_dict = queries.get_weather_data(city_name, specified_date)
    weather_icon = weather.determine_icon_based_on_weather(weather_dict)
    rain_prediction = predictions.predict_rain(city_name, specified_date)
    
    try:
        # Convert date from YYYY-MM-DD into Month DD, YYYY    
        weather_dict['date'] = datetime.strptime(weather_dict['date'], '%Y-%m-%d').strftime('%B %d, %Y')
    except:
        # If date is empty do nothing, this is handled in the html
        pass
    
    return render_template(
        "index.html.jinja",
        weather_dict = weather_dict,
        weather_icon = weather_icon,
        rain_prediction = rain_prediction)


@views_bp.route('/weather_summary')
@login_required
def weather_summary():

    # migth seem unecessary but is passed as param at end of method
    url_args = {
        'city_name' : request.args.get('city_name'),
        'date' : request.args.get('date')
    }

    if url_args['city_name'] == None:
        user_id = g.user['userId']
        url_args['city_name'] = queries.get_user_city(user_id)
        url_args['date'] = datetime(2017, 6, 24).strftime('%Y-%m-%d')

    city_name = url_args['city_name']
    date = url_args['date']

    # Prepare most of the render_template args
    weather_dict = queries.get_weather_data( city_name, date)
    weather_icon = weather.determine_icon_based_on_weather(weather_dict)
    rain_prediction = predictions.predict_rain(city_name, date)
    graph_html = graphs.get_7_day_temp_graph_html(city_name, date)
    
    try:
        # Convert date from YYYY-MM-DD into Month DD, YYYY    
        weather_dict['date'] = datetime.strptime(weather_dict['date'], '%Y-%m-%d').strftime('%B %d, %Y')
    except:
        # If date is empty do nothing, this is handled in the html
        pass
        
    return render_template(
        "features/weather_summary.html.jinja",
        weather_dict = weather_dict,
        rain_prediction = rain_prediction,
        weather_icon = weather_icon,
        graph_html = graph_html,
        url_args = url_args)

@views_bp.route('/map')
@login_required
def map():
    return render_template("features/map.html.jinja")

@views_bp.route('/graphs')
def graph():

    url_args = {
        'stat' : request.args.get('stat'),
        'city_name' : request.args.get('city_name'),
        'start_date' : request.args.get('start_date'),
        'end_date' : request.args.get('end_date')
    }
    
    for arg_val in url_args.values():
        if arg_val == None:
            graph_html = graphs.get_graph_html()
            break
    else:
        graph_html = graphs.get_graph_html(url_args)

    return render_template(
        "features/graphs.html.jinja", 
        graph_html = graph_html,
        url_args = url_args)

@views_bp.route('/location_select')
@login_required
def location_select():
    return render_template("features/location_select.html.jinja")

# -----------------
#This page is used only to determine which weather icon to use on the map as a marker
@views_bp.route('/api/weather_icon')
def get_weather_icon():
    city_name = request.args.get('cityName')
    date = request.args.get('date')
    
    weather_dict = queries.get_weather_data(city_name, date)
    
    icon_name = weather.determine_icon_based_on_weather(weather_dict)
    
    return jsonify({'icon': icon_name})

