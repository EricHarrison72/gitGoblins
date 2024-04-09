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
    icons,
    queries,
    predictions,
    db,
)
from .auth import login_required
from datetime import datetime, timedelta

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
@login_required
def index():
    user_id = g.user['userId']
    city_name = queries.get_user_city(user_id)
    specified_date = datetime(2017, 6, 24).strftime('%Y-%m-%d')

    weather_dict = queries.get_weather_data(city_name, specified_date)
    weather_icon = icons.determine_icon_based_on_weather(weather_dict)
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

    # might seem unecessary but is passed as param at end of method
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
    weather_icon = icons.determine_icon_based_on_weather(weather_dict)
    rain_prediction = predictions.predict_rain(city_name, date)
    
    # prepare graph
    try:
        date_arg = datetime.strptime(date, '%Y-%m-%d')
        start_date = (date_arg - timedelta(days=7)).strftime('%Y-%m-%d')
        
        graph_args = {
            'city_name' : city_name,
            'start_date' : start_date,
            'end_date' : date
        }
        
        graph = graphs.TemperatureGraph(graph_args)
        graph.fig.update_layout(
            height=300
        )
        graph_html = graph.get_html()

    except: 
        graph_html = "Error generating graph."
    
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
@login_required
def graph():

    url_args = {
        'stat' : request.args.get('stat'),
        'city_name' : request.args.get('city_name'),
        'start_date' : request.args.get('start_date'),
        'end_date' : request.args.get('end_date')
    }

    if None in url_args.values():
        user_id = g.user['userId']
        url_args['stat'] = "wind"
        url_args['city_name'] = queries.get_user_city(user_id)

        url_args['start_date'] = datetime(2016, 6, 24).strftime('%Y-%m-%d')
        url_args['end_date'] = datetime(2017, 6, 24).strftime('%Y-%m-%d')

    graph_html = graphs.get_graph_html(url_args)

    return render_template(
        "features/graphs.html.jinja", 
        graph_html = graph_html,
        url_args = url_args)

# -----------------
#This page is used only to determine which weather icon to use on the map as a marker
@views_bp.route('/api/weather_icon')
def get_weather_icon():
    city_name = request.args.get('cityName')
    date = request.args.get('date')
    
    weather_dict = queries.get_weather_data(city_name, date)
    icon_name = icons.determine_icon_based_on_weather(weather_dict)
    
    return jsonify({'icon': icon_name})

# ---------------
@views_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Get form data
        email_list = request.form.get('emailList') == 'on'  # Checkbox value
        city_id = int(request.form.get('cityId'))

        # Update user settings in the database
        try:
            user_id = g.user['userId']  # Get user ID from g.user
            db.update_user_settings(user_id,  email_list, city_id)
            # Redirect to index after successful update
            return redirect(url_for('views.index'))
        except Exception as e:
            error_message = 'An error occurred while updating user settings: {}'.format(str(e))
            return render_template('error.html', error_message=error_message)

    # If method is GET, render the settings page
    # You need to pass user data and city data to the template
    user_id = g.user['userId']  # Get user ID from g.user
    user = db.get_user_settings(user_id)  # Get user data from database
    cities = db.get_cities()  # Get city data from database

    return render_template('settings.html.jinja', user=user, cities=cities)
