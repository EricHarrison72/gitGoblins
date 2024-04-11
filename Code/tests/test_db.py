# -------------------------------------------------
# test_db.py
'''
Unit tests for the database (and also the test database)
'''
'''
Starter Code sources:
- [Flask docs tutorial: Test Coverage](https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/) (newer commits)
'''
# -------------------------------------------------
import sqlite3
import pytest
from weatherApp.db import get_db, _populate_db

# --------------------------
# TESTING for TESTING
# Checks if the test db is populated with the INSERT statements from the data.sql file
def test_test_db(app):
    with app.app_context():
        weather_db = get_db().execute('''
            SELECT City.cityName AS city_name, WeatherInstance.date, WeatherInstance.tempMax AS temp_high, 
                WeatherInstance.tempMin AS temp_low, WeatherInstance.rainfall, 
                rainToday AS raining, WeatherInstance.windGustSpeed AS wind_speed, 
                WeatherInstance.windGustDir AS wind_dir
            FROM WeatherInstance
            JOIN City ON WeatherInstance.cityId = City.cityId
            WHERE City.cityName = ? AND WeatherInstance.date = ?
        ''', ('Springfield','2023-01-01')).fetchone()
        
        user_db = get_db().execute('''
            SELECT userId, firstName, lastName, email, emailList, password
            FROM User
            WHERE userId = ? AND email = ?
        ''', ('1','homer@example.com')).fetchone()
        
    assert weather_db != None
    assert user_db != None

#------------------------------
    
# Test getting and closing db
'''
Within an application context, get_db should return
the  same connection each time it’s called. After 
the context, the connection should be closed.
'''
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

# test using init-db command
'''
The init-db command should call the init_db function and output a message.
'''
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('weatherApp.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
    
# test populate_db function
'''
The populate_db function should fill the database with data from the weatherAUS.csv file.
'''
def test_populate_db(app):
    with app.app_context():
        db1 = get_db() #Creating 2 databases so I can test the first and last row of database for edge cases
        db2 = get_db()
        _populate_db()
        
        db1.execute('''
            SELECT City.cityName AS city_name, WeatherInstance.date, WeatherInstance.tempMax AS temp_high, 
                WeatherInstance.tempMin AS temp_low, WeatherInstance.rainfall, 
                rainToday AS raining, WeatherInstance.windGustSpeed AS wind_speed, 
                WeatherInstance.windGustDir AS wind_dir
            FROM WeatherInstance
            JOIN City ON WeatherInstance.cityId = City.cityId
            WHERE City.cityName = ? AND WeatherInstance.date = ?
        ''', ('Albury','2008-12-01')).fetchone()
        
        db2.execute('''
            SELECT City.cityName AS city_name, WeatherInstance.date, WeatherInstance.tempMax AS temp_high, 
                WeatherInstance.tempMin AS temp_low, WeatherInstance.rainfall, 
                rainToday AS raining, WeatherInstance.windGustSpeed AS wind_speed, 
                WeatherInstance.windGustDir AS wind_dir
            FROM WeatherInstance
            JOIN City ON WeatherInstance.cityId = City.cityId
            WHERE City.cityName = ? AND WeatherInstance.date = ?
        ''', ('Uluru','2017-06-25')).fetchone()
    assert db1 != None
    assert db2 != None
    
# test_db.py

import pytest
from weatherApp import db

# Test updating user settings in the database
def test_update_user_settings_db(app, client):
    with app.app_context():
        # Register a new user with valid data including city_id
        response = client.post('/auth/register', data={
            'email': 'test@gmail.com',
            'password': 'a',
            'city_id': '1'  # Assuming city_id is provided in the form data
        })
        assert response.status_code == 302  # Check if registration is successful and redirects

        # Update user settings in the database
        user_id = 1  # Assuming user ID
        email_list = True  # New value for email list subscription
        city_id = 2  # New city ID
        db.update_user_settings(user_id, email_list, city_id)

        # Fetch updated user settings from the database
        updated_user_settings = db.get_user_settings(user_id)

        # Add assertions to verify if user settings are updated correctly
        assert updated_user_settings['emailList'] == email_list
        assert updated_user_settings['cityId'] == city_id
