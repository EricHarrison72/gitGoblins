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
            temp_high = float(request.form['temp_high'])
            specified_date = request.form['date']  # Set date using specified format
            print(city_id)
            print(temp_high)
            # Update high temperature using UPDATE statement
            datb.execute('''
                UPDATE WeatherInstance
                SET tempMax = ?
                WHERE cityId = ? AND date = ?
            ''', (temp_high, city_id, specified_date))

            # Commit the changes to the database
            datb.commit()

            # Redirect to weather_summary route with cityId and date parameters
            return redirect(url_for('views.weather_summary', city_id=city_id, date=specified_date))
    except ValueError as ve:
        error_message = 'Invalid input value: {}'.format(str(ve))
        return jsonify({'error': error_message}), 400
    except Exception as e:
        error_message = 'An error occurred while updating high temperature: {}'.format(str(e))
        return jsonify({'error': error_message}), 500