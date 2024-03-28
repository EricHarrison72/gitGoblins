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
# ------------------------------------------------
import pytest
from flask import session
from weatherApp import views

# Test the weather_summary view when logged in
def test_weather_summary_authenticated(client, app):
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

        # Access the weather summary page (assuming '/weather_summary' is the URL for the weather summary)
        response_summary = client.get('/weather_summary')
        assert response_summary.status_code == 200  # Check if the weather summary page is accessible

        # Add assertions for the content of the weather summary page if needed


def test_weather_summary_not_authenticated(client, app):
    with client:
        response = client.get('/weather_summary')
        assert response.status_code == 302  # Redirect to login
        assert response.headers['Location'].endswith('/auth/login')

# Test if the map page renders successfully
def test_map(client, app):
    with client:
        # Register a new user with valid data including city_id
        response = client.post('/auth/register', data={
            'email': 'test@gmail.com',
            'password': 'a',
            'city_id': '1'  # Assuming city_id is provided in the form data
        })
        assert response.status_code == 302  # Check if registration is successful and redirects

        # Follow the redirection to the map page
        response = client.get('/map', follow_redirects=True)
        assert response.status_code == 200  # Check if it successfully loads the map page

        

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