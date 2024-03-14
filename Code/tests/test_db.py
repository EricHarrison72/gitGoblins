# -------------------------------------------------
# test_db.py
'''
This code provides a basic user authentication system for a Flask web application, 
including user registration, login, and logout functionalities.
The login_required decorator can be applied to views that require authentication to restrict access.
'''
'''
Starter Code sources:
- [Flask docs tutorial: Test Coverage](https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/) (newer commits)
'''
# -------------------------------------------------
import sqlite3
import pytest
from weatherApp.db import get_db, populate_db

# check if the test db is populated
def test_test_db(app):
    with app.app_context():
        db = get_db().execute('''
            SELECT City.cityName AS city_name, WeatherInstance.date, WeatherInstance.tempMax AS temp_high, 
                WeatherInstance.tempMin AS temp_low, WeatherInstance.rainfall, 
                rainToday AS raining, WeatherInstance.windGustSpeed AS wind_speed, 
                WeatherInstance.windGustDir AS wind_dir
            FROM WeatherInstance
            JOIN City ON WeatherInstance.cityId = City.cityId
            WHERE City.cityName = ? AND WeatherInstance.date = ?
        ''', ('Albury','2008-12-01')).fetchone()

    assert db != None

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