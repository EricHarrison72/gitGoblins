# ------------------------------------------------
# test_views.py
'''
Contains unit tests for the views.py
'''
'''
Starter Code sources:
- [Flask Docs - test client](https://flask.palletsprojects.com/en/3.0.x/testing/#sending-requests-with-the-test-client)
'''
# ------------------------------------------------
import pytest
from weatherApp import views
from weatherApp.db import get_db

# THE MAIN TEST LOGIC IS WRITTEN HERE
class ViewTests:
    def test_not_authenticated(client, url):
        with client:
            view_response = client.get(url)
            assert view_response.status == '302 FOUND'
            assert view_response.location.endswith('/auth/login')

    def test_authenticated(client, url, expected_html_elem):
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

# THE TESTS (for reals)
# -------------------
'''NOTE 1
The reason each test is seperated out like this (even though it
seems like it violates DRY) is because the client fixture needs
to get torn down and reset between tests.
'''
'''NOTE 2
Note the format of expected_html_elem: 'Page Title\n -'.
This element is expected in the page because that is consistently
the format in the title blocks of the templates. The following 
alternatives are less reliable:
    - 'Page Title' ... this might show up on pages other than the one you're testing
    - '<h1>Page Title</h1>' or other tags ... formatting within tags varies between templates
'''
# HOME
def test_index__not_authenticated(client):
    ViewTests.test_not_authenticated(client, '/')

# TODO @Chase or @Eric why does this fail??
def test_index__authenticated(client):
    ViewTests.test_authenticated(client, '/', 'Home\n -')

# FEATURES
def test_weather_summary__not_authenticated(client):
    ViewTests.test_not_authenticated(client, '/weather_summary')

def test_weather_summary__authenticated(client):
    ViewTests.test_authenticated(client,'/weather_summary', 'Weather Summary\n -')

def test_map__not_authenticated(client):
    ViewTests.test_not_authenticated(client, '/map')

def test_map__authenticated(client):
    ViewTests.test_authenticated(client, '/map', 'Map\n -') 

# TODO idk why but the graph tests are failing for some reason
def test_graph__not_authenticated(app, client):
    with app.app_context():
        ViewTests.test_not_authenticated(client, '/graphs')

def test_graph__authenticated(app, client):
    with app.app_context():
        ViewTests.test_authenticated(client, '/graphs', 'Graph\n -')

# OTHER
def test_settings__not_authenticated(client):
    ViewTests.test_not_authenticated(client, '/settings')

def test_settings__authenticated(client):
    ViewTests.test_authenticated(client, '/settings', 'Settings\n -')

def test_get_weather_icon(client):
    with client:
        response = client.get('/api/weather_icon?cityName=Sydney&date=2024-03-20')
        assert response.status == '200 OK'

# TODO THIS TEST SHOULDN'T BE HERE
'''
The whole organization of user settings needs to be addressed in another branch
  -- the fix_view_tests branch
'''
# def test_update_user_settings(client, app):
#     with client:
#         # Register a new user with valid data including city_id
#         response = client.post('/auth/register', data={
#             'email': 'test@gmail.com',
#             'password': 'a',
#             'city_id': '1'  # Assuming city_id is provided in the form data
#         })
#         assert response.status_code == 302  # Check if registration is successful and redirects

#         # Log in the registered user
#         response_login = client.post('/auth/login', data={
#             'email': 'test@gmail.com',
#             'password': 'a'
#         })
#         assert response_login.status_code == 302  # Check if login is successful and redirects

#         # Update user settings
#         response_update = client.post('/settings', data={
#             'emailList': 'on',
#             'cityId': '2'  # Assuming new city_id
#         })
#         assert response_update.status_code == 302  # Check if update is successful and redirects
