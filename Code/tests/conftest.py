# -------------------------------------------------
# conftest.py
'''
Configuration file for unit testing our flask app.
Contains fixtures that all tests will need.
'''
# -------------------------------------------------
import pytest
from weatherApp import create_app, db

@pytest.fixture()
def app():
    app = create_app("sqlite://")

    with app.app_context():
        db.init_db()

    yield app 
    # everything after this would be teardown

@pytest.fixture()
def client(app):
    # allows us to simulate requests to the app
    app.test_client()