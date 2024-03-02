#app.py

# NOTE: This file exists to help us start us out. 
# We may want to break our app into several python files for different components later on.
from flask import Flask, render_template
from flaskr import create_app, db

#app = Flask(__name__) -- This line doesn't work as is, but if we figure it out we won't need to re-initialize the database everytime we run it
app = create_app() #Re-initializes entire database every time we run this :/

@app.route('/')
def hello_world():
    message = "Hello World!"
    return render_template("index.html", message=message)

@app.route('/weather_summary')
def weather_summary():
    datb = db.get_db()

    city_id = 1 #City set to 1, as there's no way of collecting specific city id from webpage yet

    #SQL query to get data for specific city (query isn't correct right now)
    weather_data = datb.execute('''
        SELECT City.cityName, WeatherInstance.date, WeatherInstance.tempMax AS temp_high, 
               WeatherInstance.tempMin AS temp_low, WeatherInstance.rainfall, 
               WeatherInstance.rainfall > 0 AS raining, WeatherInstance.windSpeed, 
               WeatherInstance.windDir
        FROM WeatherInstance
        JOIN City ON WeatherInstance.cityId = City.cityId
        WHERE WeatherInstance.cityId = ?
        ORDER BY WeatherInstance.date DESC
        LIMIT 1
    ''', (city_id,)).fetchone()

    if weather_data is None:
        # Handle the case where no weather data is found
        weather_list = ["No data", "N/A", 0, 0, 0.0, False, 0, "N/A"]
    else:
        weather_list = [
            weather_data['cityName'], 
            weather_data['date'], 
            weather_data['temp_high'], 
            weather_data['temp_low'], 
            weather_data['rainfall'], 
            weather_data['raining'], 
            weather_data['windSpeed'], 
            weather_data['windDir']
        ]
    
    return render_template("weather_summary.html", weather_list=weather_list)


if __name__ == "__main__":
    app.run(debug=True)
