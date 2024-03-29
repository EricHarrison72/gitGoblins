from datetime import datetime
from flask import Blueprint, request, jsonify, redirect, url_for
from . import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['POST'])
def admin():
    try:
        datb = db.get_db()
        if request.method == 'POST':
            city_id = int(request.form['city_id'])
            temp_min = float(request.form['tempMin'])
            temp_max = float(request.form['tempMax'])
            specified_date = request.form['date']  
            sunshine_value = float(request.form['sunshine'])
            rainfall_value = float(request.form['rainfall'])
            evaporation_value = float(request.form['evaporation'])
            cloud9am_value = int(request.form['cloud9am'])
            cloud3pm_value = int(request.form['cloud3pm'])
            pressure9am_value = float(request.form['pressure9am'])
            pressure3pm_value = float(request.form['pressure3pm'])
            humidity9am_value = int(request.form['humidity9am'])
            humidity3pm_value = int(request.form['humidity3pm'])
            windGustSpeed_value = int(request.form['windGustSpeed'])
            windGustDir_value = request.form['windGustDir']
            windSpeed9am_value = int(request.form['windSpeed9am'])
            windSpeed3pm_value = int(request.form['windSpeed3pm'])
            windDir9am_value = request.form['windDir9am']
            windDir3pm_value = request.form['windDir3pm']
            rainToday_value = bool(request.form['rainToday'])
            rainTomorrow_value = bool(request.form['rainTomorrow'])

            # Fetch cityName from cityId
            cursor = datb.execute("SELECT cityName FROM City WHERE cityId = ?", (city_id,))
            city_name = cursor.fetchone()[0]

            # Update all columns in WeatherInstance table
            datb.execute('''
                UPDATE WeatherInstance
                SET tempMin = ?, tempMax = ?, sunshine = ?, rainfall = ?, evaporation = ?, cloud9am = ?, cloud3pm = ?,
                    pressure9am = ?, pressure3pm = ?, humidity9am = ?, humidity3pm = ?, windGustSpeed = ?,
                    windGustDir = ?, windSpeed9am = ?, windSpeed3pm = ?, windDir9am = ?, windDir3pm = ?,
                    rainToday = ?, rainTomorrow = ?
                WHERE cityId = ? AND date = ?
            ''', (temp_min, temp_max, sunshine_value, rainfall_value, evaporation_value, cloud9am_value, cloud3pm_value,
                  pressure9am_value, pressure3pm_value, humidity9am_value, humidity3pm_value, windGustSpeed_value,
                  windGustDir_value, windSpeed9am_value, windSpeed3pm_value, windDir9am_value, windDir3pm_value,
                  rainToday_value, rainTomorrow_value, city_id, specified_date))

            # Commit the changes to the database
            datb.commit()

            # Redirect to weather_summary route with cityName and date parameters
            return redirect(url_for('views.weather_summary', city_name=city_name, date=specified_date))
    except ValueError as ve:
        error_message = 'Invalid input value: {}'.format(str(ve))
        return jsonify({'error': error_message}), 400
    except Exception as e:
        error_message = 'An error occurred while updating high temperature: {}'.format(str(e))
        return jsonify({'error': error_message}), 500
