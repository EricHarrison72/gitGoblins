# -------------------------------------------------
# conftest.py
'''
Configuration file for unit testing our flask app.
Contains fixtures that all tests will need.
'''
'''
Starter Code sources:
- [Flask docs tutorial: Test Coverage](https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/) (newer commits)
- [Getting Started With Testing in Flask](https://www.youtube.com/watch?v=RLKW7ZMJOf4) (older commits)
'''
# -------------------------------------------------
import os
import tempfile

import pytest
from weatherApp import create_app
from weatherApp.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture()
def app():
    # open a temporary file for test data
    db_fd, db_path = tempfile.mkstemp()

    # Create an app instance in test mode
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app 

    # teardown
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture()
def client(app):
    # allows us to simulate requests to the app
    return app.test_client()

@pytest.fixture()
def runner(app):
    # creates a runner that can call the Click commands registered with the application
    return app.test_cli_runner()