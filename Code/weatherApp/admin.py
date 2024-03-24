'''admin.py'''

from flask import Blueprint, request, jsonify
from . import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['POST'])
def admin():
    data = request.json

    city_id = data.get('city_id')
    date = data.get('date')
    temp_high = data.get('temp_high')
    temp_low = data.get('temp_low')
    rainfall = data.get('rainfall')
    raining = data.get('raining')
    wind_speed = data.get('wind_speed')
    wind_dir = data.get('wind_dir')
    cloud = data.get('cloud')

    db.execute('''
        INSERT INTO WeatherInstance (cityId, date, tempMax, tempMin, rainfall, rainToday, windGustSpeed, windGustDir, cloud3pm)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(cityId, date) DO UPDATE SET 
            tempMax=excluded.tempMax, 
            tempMin=excluded.tempMin, 
            rainfall=excluded.rainfall, 
            rainToday=excluded.rainToday, 
            windGustSpeed=excluded.windGustSpeed, 
            windGustDir=excluded.windGustDir, 
            cloud3pm=excluded.cloud3pm
    ''', (city_id, date, temp_high, temp_low, rainfall, raining, wind_speed, wind_dir, cloud))

    return jsonify({'message': 'Weather data updated successfully'}), 200
