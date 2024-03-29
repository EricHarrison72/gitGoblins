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
            

            # Fetch cityName from cityId
            cursor = datb.execute("SELECT cityName FROM City WHERE cityId = ?", (city_id,))
            city_name = cursor.fetchone()[0]

            # Update all columns in WeatherInstance table
            datb.execute('''
                UPDATE WeatherInstance
                SET tempMin = ?, tempMax = ?
                WHERE cityId = ? AND date = ?
            ''', (temp_min, temp_max, city_id, specified_date))

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
