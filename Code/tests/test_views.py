# ------------------------------------------------
# test_views.py
'''
This currently exists to test (mostly front end stuff) in views.py
In the future we will create several test files. (see test_example)
'''
'''
Starter Code sources:
- [Getting Started With Testing in Flask](https://www.youtube.com/watch?v=RLKW7ZMJOf4)
'''
'''
Refactoring notes:
- we already have tests users in the test db... do we really need to register a new user for each test??
'''
# ------------------------------------------------
import pytest
from weatherApp import views
from weatherApp.db import get_db

# HTTP status codes
PAGE_OK = 200
PAGE_FOUND = 302

# THE MAIN TEST LOGIC IS WRITTEN HERE
class ViewTests:
    def test_not_authenticated(client, url):
        with client:
            view_response = client.get(url)
            assert view_response.status == '302 FOUND'
            assert view_response.location.endswith('/auth/login')

    def test_authenticated(app, client, url, expected_html_elem):
        with app.app_context():
            with client:

                register_test_user(client)
                login_test_user(client)

                view_response = client.get( url)

                assert view_response.status == '200 OK'
                assert expected_html_elem.encode("utf-8") in view_response.data 

# Helpers for test_authenticated
def register_test_user(client):
    client.post(
        '/auth/register',
        data = {
            'email': 'test@gmail.com',
            'password': 'a',
            'city_id': '1'
        }
    )

def login_test_user(client):
    client.post(
        '/auth/login',
        data = {
            'email': 'test@gmail.com',
            'password': 'a'
        }
    )
# ----------------------

# THE TESTS (for reals)
# -------------------
'''
The reason each test is seperated out like this (even though it
seems like it violates DRY) is because the client fixture needs
to get torn down and reset between tests.
'''
def test_weather_summary__not_authenticated(client):
    ViewTests.test_not_authenticated(client, '/weather_summary')

def test_weather_summary__authenticated(app, client):
    ViewTests.test_authenticated(app, client,'/weather_summary', '<h1>\n  Weather Summary')

def test_map__not_authenticated(client, app):
    ViewTests.test_not_authenticated(client, '/map')

############################################################
# Test if the location_select page renders successfully
def test_location_select(client, app):
    with client:
        # Register a new user with valid data including city_id
        response = client.post('/auth/register', data={
            'email': 'test@gmail.com',
            'password': 'a',
            'city_id': '1'  # Assuming city_id is provided in the form data
        })
        assert response.status_code == 302  # Check if registration is successful and redirects

        # Access the location_select page
        response = client.get('/location_select')
        assert response.status_code == 302
        
# Test if the weather_icon API returns a valid response
def test_get_weather_icon(client, app):
    with client:
        # Access the weather_icon API
        response = client.get('/api/weather_icon?cityName=Sydney&date=2024-03-20')
        assert response.status_code == 200
        
# Test if the index page renders successfully
def test_index(client, app):
    with client:
        # Register a new user with valid data including city_id
        response = client.post('/auth/register', data={
            'email': 'test@gmail.com',
            'password': 'a',
            'city_id': '1'  # Assuming city_id is provided in the form data
        })
        assert response.status_code == 302  # Check if registration is successful and redirects

        # Access the index page
        response = client.get('/')
        assert response.status_code == 302
   #graph.py is currently being worked on so this test isn't complete     
"""
def test_graph(client, app):
   with client:
      response = client.get('/graph')
      assert response.status_code == 302
   """
# Test if the settings page renders successfully
def test_settings(client, app):
    with client:
        # Register a new user with valid data including city_id
        response = client.post('/auth/register', data={
            'email': 'test@gmail.com',
            'password': 'a',
            'city_id': '1'  # Assuming city_id is provided in the form data
        })
        assert response.status_code == 302  # Check if registration is successful and redirects

        # Log in the registered user
        response_login = client.post('/auth/login', data={
            'email': 'test@gmail.com',
            'password': 'a'
        })
        assert response_login.status_code == 302  # Check if login is successful and redirects

        # Access the settings page
        response_settings = client.get('/settings')
        assert response_settings.status_code == 200  # Check if the settings page is accessible

   
   # Test updating user settings
def test_update_user_settings(client, app):
    with client:
        # Register a new user with valid data including city_id
        response = client.post('/auth/register', data={
            'email': 'test@gmail.com',
            'password': 'a',
            'city_id': '1'  # Assuming city_id is provided in the form data
        })
        assert response.status_code == 302  # Check if registration is successful and redirects

        # Log in the registered user
        response_login = client.post('/auth/login', data={
            'email': 'test@gmail.com',
            'password': 'a'
        })
        assert response_login.status_code == 302  # Check if login is successful and redirects

        # Update user settings
        response_update = client.post('/settings', data={
            'emailList': 'on',
            'cityId': '2'  # Assuming new city_id
        })
        assert response_update.status_code == 302  # Check if update is successful and redirects
