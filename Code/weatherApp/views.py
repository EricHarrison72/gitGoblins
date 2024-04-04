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
from datetime import datetime, timedelta

views_bp = Blueprint('views', __name__)

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
    specified_date = datetime(2017, 6, 24).strftime('%Y-%m-%d')

    # Fetch the WeatherInstance data for the specified date (March 25, 2017)
    weather_data = datb.execute(
        "SELECT * FROM WeatherInstance WHERE cityId = ? AND date = ?",
        (user_city_data['cityId'], specified_date)
    ).fetchone()
    
    # Fetch cityName from the City table for specific cityId
    city_name_row = datb.execute(
    "SELECT cityName FROM City WHERE cityId = ?",
    (user_city_data['cityId'],)
    ).fetchone()

    # Extract the cityName string from the row object
    city_name = city_name_row['cityName']

    # Get the main weather icon for this city/date
    weather_dict = queries.get_weather_data(city_name, specified_date)
    weather_icon = weather.determine_icon_based_on_weather(weather_dict)
    
    return render_template("index.html.jinja", user_city_data=user_city_data, weather_data=weather_data, weather_icon=weather_icon)


@views_bp.route('/weather_summary')
@login_required
def weather_summary():

    url_args = {
        'city_name' : request.args.get('city_name'),
        'date' : request.args.get('date')
    }

    # Dictionary of weather data
    weather_dict = queries.get_weather_data(url_args['city_name'], url_args['date'])
    
    # AI prediction for rain
    rain_prediction = predictions.predict_rain(url_args['city_name'], url_args['date'])
    
    # Weather icon for most prominent weather feature
    weather_dict = queries.get_weather_data(url_args['city_name'], url_args['date'])
    weather_icon = weather.determine_icon_based_on_weather(weather_dict)
    
    try:
        # Convert 'date' URL argument to datetime object
        date_arg = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
        # Calculate the start_date as 7 days before the 'date'
        start_date = (date_arg - timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Get arguments to create graph of previous week
        graph_args = {
            'stat' : 'temperature',
            'city_name' : url_args['city_name'],
            'start_date' : start_date,
            'end_date' : url_args['date']
        }
        
        # Generate temperature graph for previous week
        for arg_val in graph_args.values():
            if arg_val == None:
                figure_html = graphs.get_graph_html()
                break
        else:
            figure_html = graphs.get_graph_html(graph_args)
    # If there is no data for this city/date set the graph to None
    except: 
        figure_html = None
    
    try:
        # Convert date from YYYY-MM-DD into Month DD, YYYY    
        weather_dict['date'] = datetime.strptime(weather_dict['date'], '%Y-%m-%d').strftime('%B %d, %Y')
    except:
        # If date is empty do nothing, this is handles in the html
        None
        
    return render_template(
        "features/weather_summary.html.jinja",
        weather_dict = weather_dict,
        rain_prediction = rain_prediction,
        weather_icon = weather_icon,
        figure_html = figure_html,
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
            figure_html = graphs.get_graph_html()
            break
    else:
        figure_html = graphs.get_graph_html(url_args)

    return render_template(
        "features/graphs.html.jinja", 
        figure_html = figure_html,
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
