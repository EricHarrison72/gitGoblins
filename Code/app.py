# NOTE: This file exists to help us start us out. 
# We may want to break our app into several python files for different components later on.
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    message = "Hello World!"
    return render_template("index.html", message=message)

@app.route('/weather_summary')
def weather_summary():
    location = "Location Name"
    date = "Date"
    temp_high = 25
    temp_low = 10
    precipitation = 12.3
    raining = True
    wind_speed = 10
    wind_dir = "NW"
    weather_list = [location,date,temp_high,temp_low,precipitation,raining,wind_speed,wind_dir]
    return render_template("weather_summary.html", weather_list=weather_list)

if __name__ == "__main__":
    app.run(debug=True)
