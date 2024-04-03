'''admin.py'''

from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from . import db, notification, queries

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET','POST'])
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


@admin_bp.route('/admin_alert', methods=['GET', 'POST'])
def admin_alert():
    url_args = {"date": '2017-06-24'}

    try:
        datb = db.get_db()
        if request.method == 'POST':
            event = request.form.get('eventSelect')
            city = request.form.get('citySelect')

            if city != None:
                city.replace(' ', '') # (just in case)

            date = '2016-01-01'

            url_args['date'] = date

            # Put the arguments into a list to pass into get_template
            event_args = {
                "city_name": city,
                "date": date,
                "data_point": event
            }
            
            # Send the notification
            notification.send_email(
                queries.get_alert_emails(city),
                city,
                notification.get_template
            )
            
                
            flash('Alert sent. City: ' + city + '. Event: ' + event + '. Date: ' + date)
            return redirect(url_for('admin.admin_alert'))
    except ValueError:
        flash('Error in sending alert. Please check parameters.')
        return redirect(url_for('admin.admin_alert'))
    
    return render_template('admin_dashboard.html.jinja', url_args = url_args)
