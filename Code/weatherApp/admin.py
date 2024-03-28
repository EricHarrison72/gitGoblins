'''admin.py'''

from flask import Blueprint, request, jsonify
from . import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['POST'])
def admin():
    data = request.form

    city_name = data.get('city_name')
    date = data.get('date')
    temp_high = data.get('temp_high')

    try:
        # Retrieve the cityId corresponding to the provided city name
        city_id = db.get_db().execute('SELECT cityId FROM City WHERE cityName = ?', (city_name,)).fetchone()
        if city_id is not None:
            city_id = city_id[0]  # Extract cityId from the result tuple

            # Update high temperature
            print(city_id)
            print(temp_high)
            db.execute('''
                INSERT INTO WeatherInstance (cityId, date, tempMax)
                VALUES (?, ?, ?)
                ON CONFLICT(cityId, date) DO UPDATE SET 
                    tempMax=excluded.tempMax
            ''', (city_id, date, temp_high))

            return jsonify({'message': 'High temperature updated successfully'}), 200
        else:
            return jsonify({'error': 'City not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
