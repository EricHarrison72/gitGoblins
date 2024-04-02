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
from flask import Flask
from weatherApp import views
from weatherApp.db import get_db

# @pytest.fixture()
# def register_data():
#     return {
#         'email': 'test@gmail.com',
#         'password': 'a',
#         'city_id': '1'  # Assuming city_id is provided in the form data
#     }

# @pytest.fixture()
# def login_response(client):
#     '''
#     Returns a response object
#     '''
#     with client:
#         login_response = client.post(
#             '/auth/login',
#             data = {
#                 'email': 'homer@example.com',
#                 'password': 'password123'
#             }
#         )

#     return login_response

# HTTP status codes
PAGE_OK = 200
PAGE_FOUND = 302

# THE MAIN TEST LOGIC IS WRITTEN HERE
class ViewTests:
    def __init__(self, client, app: Flask, url: str, expected_html_element: str):
        self.client = client
        self.app = app
        self.url = url
        self.expected_html_element = expected_html_element

    def test_authenticated(self):
        with self.app.app_context():
            with self.client:

                login_response = self.client.post(
                    '/auth/login',
                    data = {
                        'email': 'homer@example.com',
                        'password': 'password123'
                    }
                )
                assert login_response.status_code == PAGE_FOUND # TODO: once stuff is working, remove this line

                response = self.client.get( self.url)

                assert response.status_code == PAGE_OK 
                assert self.expected_html_element in response.data 

    def test_not_authenticated(self):
        with self.client:
            response = self.client.get(self.url)
            assert response.status_code == PAGE_FOUND 
            assert response.headers['Location'].endswith('/auth/login')

# HELPER
def run_view_tests(client, app, url, html_elem):
    view_tests = ViewTests(
        client,
        app,
        url,
        html_elem
    )
    view_tests.test_authenticated()
    view_tests.test_not_authenticated()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# TODO TODO TODO 
'''
ALRIGHT FINE FUCK FINE DUDE
EITHER:
1. Find a way to hash the test users' passwords in conftest
OR
2. Clean up Chase's approach and use that
'''
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# ===========================================================

# THE TESTS (for reals)
# -------------------
def test_weather_summary_view(client, app):
    run_view_tests(client, app, '/weather_summary', '<h1>Weather Summary</h1>')

def test_map_view(client, app):
    run_view_tests(client, app, '/map', '<h1>Map</h1>') # make sure follow redirects is true



# def test_map(client, app):
#     with client:
#         # Register a new user with valid data including city_id
#         response = client.post('/auth/register', data={
#             'email': 'test@gmail.com',
#             'password': 'a',
#             'city_id': '1'  # Assuming city_id is provided in the form data
#         })
#         assert response.status_code == 302  # Check if registration is successful and redirects

#         # Follow the redirection to the map page
#         response = client.get('/map', follow_redirects=True)
#         assert response.status_code == 200  # Check if it successfully loads the map page

        

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
