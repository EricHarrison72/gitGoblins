# -------------------------------------------------
# test_db.py
'''
Unit tests for the database
'''
'''
Starter Code sources:
- [Flask docs tutorial: Test Coverage](https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/) (newer commits)
'''
# -------------------------------------------------
import sqlite3
import pytest
from weatherApp.db import get_db, populate_db

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

# test using inti-db command
'''
The init-db command should call the init_db function and output a message.
It's kinda weird that this test passes when we can't even figure that code out ourselves.
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