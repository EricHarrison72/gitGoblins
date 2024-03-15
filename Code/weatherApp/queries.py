# --------------------------------------
# queries.py
'''
Contains methods to retrieve data from the database
'''
# ----------------------------------
from . import db

# retrieves weather data given city name and date
def get_weather_data (city_name, date):

    datb = db.get_db()

    #SQL query to get data for specific city
    #weather_data is an sqlite3 Row object
    weather_data_row = datb.execute('''
        SELECT City.cityName AS city_name, WeatherInstance.date, WeatherInstance.tempMax AS temp_high, 
               WeatherInstance.tempMin AS temp_low, WeatherInstance.rainfall, 
               rainToday AS raining, WeatherInstance.windGustSpeed AS wind_speed, 
               WeatherInstance.windGustDir AS wind_dir
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
        'wind_dir': '?'
        }

        # If a city name and date were passed, put that in the dict
        try:
            weather_data_dict['city_name'] += ' for ' + city_name + ' on this date'
            weather_data_dict['date'] = date
        except:
            pass

    else:
        weather_data_dict = {
        'city_name': weather_data_row['city_name'], 
        'date': weather_data_row['date'], 
        'temp_high': weather_data_row['temp_high'], 
        'temp_low': weather_data_row['temp_low'], 
        'rainfall': weather_data_row['rainfall'], 
        'raining': weather_data_row['raining'], 
        'wind_speed': weather_data_row['wind_speed'], 
        'wind_dir': weather_data_row['wind_dir']
        }

    return weather_data_dict