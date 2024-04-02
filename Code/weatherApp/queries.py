# --------------------------------------
# queries.py
'''
Contains methods to retrieve data from the database
'''
# ----------------------------------
from . import db

# retrieves weather data given city name and date
def get_weather_data (city_name, date):

    if city_name != None:
        city_name.replace(' ', '') # (just in case)

    datb = db.get_db()

    #SQL query to get data for specific city
    #weather_data is an sqlite3 Row object
    weather_data_row = datb.execute('''
        SELECT
            City.cityName AS city_name,
            WeatherInstance.date,
            WeatherInstance.tempMax AS temp_high,
            WeatherInstance.tempMin AS temp_low,
            WeatherInstance.rainfall, 
            rainToday AS raining,
            WeatherInstance.windGustSpeed AS wind_speed, 
            WeatherInstance.windGustDir AS wind_dir,
            WeatherInstance.cloud3pm AS cloud
        FROM WeatherInstance
        JOIN City ON WeatherInstance.cityId = City.cityId
        WHERE City.cityName = ? AND WeatherInstance.date = ?
    ''', (city_name,date,)).fetchone()
    
    # convert the Row to a Python dictionary
    # (so we can place the "no data" values in it if neccesary)
    if weather_data_row is None:
        # Handle the case where no weather data is found
        weather_data_dict = {
        'city_name': 'NO DATA', 
        'date': 'No Date', 
        'temp_high': 0, 
        'temp_low': 0, 
        'rainfall': 0.0, 
        'raining': '?', 
        'wind_speed': 0, 
        'wind_dir': '?',
        'cloud': 0
        }

        # If a city name and date were passed, put that in the dict
        try:
            weather_data_dict['city_name'] += ' for ' + _add_space(city_name) + ' on this date'
            weather_data_dict['date'] = date
        except:
            pass

    else:
        weather_data_dict = {
        'city_name': _add_space(weather_data_row['city_name']), 
        'date': weather_data_row['date'], 
        'temp_high': weather_data_row['temp_high'], 
        'temp_low': weather_data_row['temp_low'], 
        'rainfall': weather_data_row['rainfall'], 
        'raining': weather_data_row['raining'], 
        'wind_speed': weather_data_row['wind_speed'], 
        'wind_dir': weather_data_row['wind_dir'],
        'cloud' : weather_data_row['cloud']
        }

    return weather_data_dict

# helper method that adds a space to the city name if it should have one
# eg 'AliceSprings' -> 'Alice Springs'
def _add_space(city_name: str):

    upper_count = 0 # number of uppercase letters in city_name

    # Add spaces in front of all internal upper case characterss
    i = 1 # (we can skip checking first char
    while i in range(len(city_name)):
        if city_name[i].isupper():
            city_name = city_name[:i] + ' ' + city_name[i:]
            i += 1 # needed to skip the space

        i += 1

    return city_name

def get_temp_in_range(city_name, start_date, end_date):

    if city_name != None:
        city_name.replace(' ', '') # (just in case)

    datb = db.get_db()

    #SQL query to get data for specific city
    #weather_data is an sqlite3 Row object
    temp_in_range = datb.execute('''
        SELECT
            WeatherInstance.date, 
            WeatherInstance.tempMin AS temp_low,
            WeatherInstance.tempMax AS temp_high
        FROM WeatherInstance
        JOIN City ON WeatherInstance.cityId = City.cityId
        WHERE City.cityName = ? AND date BETWEEN ? AND ?
    ''', (city_name,start_date, end_date)).fetchall()

    return temp_in_range

def get_alert_emails(city_name):

    if city_name != None:
        city_name.replace(' ', '') # (just in case)

    datb = db.get_db()

    # SQL query to get the list of emails that are signed up for alerts for a specific city
    alert_emails = datb.execute('''
        SELECT User.email
        FROM User JOIN UsersCities ON User.userId = UsersCities.userId JOIN City ON UsersCities.cityId = City.cityId
        WHERE cityName = ? AND User.emailList = true     
    ''', (city_name,)).fetchall()

    # Convert the list of SQL rows into a list of the element in each row
    alert_emails = [i[0] for i in alert_emails]

    return alert_emails