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
            WeatherInstance.tempMin AS temp_low,
            WeatherInstance.tempMax AS temp_high,
            WeatherInstance.sunshine AS sunshine,
            WeatherInstance.rainfall AS rainfall,
            WeatherInstance.evaporation AS evaporation,
            WeatherInstance.cloud9am AS cloud_9am,
            WeatherInstance.cloud3pm AS cloud_3pm,
            WeatherInstance.pressure9am AS pressure_9am,
            WeatherInstance.pressure3pm AS pressure_3pm,
            WeatherInstance.humidity9am AS humidity_9am,
            WeatherInstance.humidity3pm AS humidity_3pm,
            WeatherInstance.windGustSpeed AS wind_speed,
            WeatherInstance.windGustDir AS wind_dir,
            WeatherInstance.windSpeed9am AS wind_speed_9am,
            WeatherInstance.windSpeed3pm AS wind_speed_3pm,
            WeatherInstance.windDir9am AS wind_dir_9am,
            WeatherInstance.windDir3pm AS wind_dir_3pm,
            WeatherInstance.rainToday AS rain_today,
            WeatherInstance.rainTomorrow AS rain_tomorrow
        FROM WeatherInstance
        JOIN City ON WeatherInstance.cityId = City.cityId
        WHERE City.cityName = ? AND WeatherInstance.date = ?
    ''', (city_name, date,)).fetchone()

    
    # convert the Row to a Python dictionary
    # (so we can place the "no data" values in it if neccesary)
    if weather_data_row is None:
        # Handle the case where no weather data is found
        weather_data_dict = {
            'city_name': 'NO DATA',
            'date': 'No Date',
            'temp_low': 0,
            'temp_high': 0,
            'sunshine': 0,
            'rainfall': 0.0,
            'evaporation': 0.0,
            'cloud_9am': 0,
            'cloud_3pm': 0,
            'pressure_9am': 0.0,
            'pressure_3pm': 0.0,
            'humidity_9am': 0,
            'humidity_3pm': 0,
            'wind_speed': 0,
            'wind_dir': '?',
            'wind_speed_9am': 0,
            'wind_speed_3pm': 0,
            'wind_dir_9am': '?',
            'wind_dir_3pm': '?',
            'rain_today': '?',
            'rain_tomorrow': '?'
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
        'temp_low': weather_data_row['temp_low'], 
        'temp_high': weather_data_row['temp_high'], 
        'sunshine': weather_data_row['sunshine'], 
        'rainfall': weather_data_row['rainfall'], 
        'evaporation': weather_data_row['evaporation'], 
        'cloud_9am': weather_data_row['cloud_9am'], 
        'cloud_3pm': weather_data_row['cloud_3pm'], 
        'pressure_9am': weather_data_row['pressure_9am'], 
        'pressure_3pm': weather_data_row['pressure_3pm'], 
        'humidity_9am': weather_data_row['humidity_9am'], 
        'humidity_3pm': weather_data_row['humidity_3pm'], 
        'wind_speed': weather_data_row['wind_speed'], 
        'wind_dir': weather_data_row['wind_dir'], 
        'wind_speed_9am': weather_data_row['wind_speed_9am'], 
        'wind_speed_3pm': weather_data_row['wind_speed_3pm'], 
        'wind_dir_9am': weather_data_row['wind_dir_9am'], 
        'wind_dir_3pm': weather_data_row['wind_dir_3pm'], 
        'rain_today': weather_data_row['rain_today'], 
        'rain_tomorrow': weather_data_row['rain_tomorrow']
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

