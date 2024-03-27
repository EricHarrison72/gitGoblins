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
        # Register a new user
        client.post('/auth/register', data={'email': 'test@gmail.com', 'password': 'a'})

        # Attempt to log in with the registered user
        response_login = client.post('/auth/login', data={'email': 'test@gmail.com', 'password': 'a'})

        # Check if login was successful
        assert response_login.status_code == 302  # Check if login was successful

        # Access the weather_summary view
        response_summary = client.get('/weather_summary')

        # Check if the response is successful
        assert response_summary.status_code == 200

def test_weather_summary_not_authenticated(client, app):
    with client:
        response = client.get('/weather_summary')
        assert response.status_code == 302  # Redirect to login
        assert response.headers['Location'].endswith('/auth/login')

# Test if the map page renders successfully
def test_map(client, app):
    with client:
        # Register a new user
        client.post('/auth/register', data={'email': 'test@gmail.com', 'password': 'a'})
        # Attempt to log in with the registered user
        response_login = client.post('/auth/login', data={'email': 'test@gmail.com', 'password': 'a'})
        # Check if login was successful
        assert response_login.status_code == 302  # Check if login was successful
        
        # Access the map page
        response = client.get('/map')
        assert response.status_code == 200
        
# Test if the weather_icon API returns a valid response
def test_get_weather_icon(client, app):
    with client:
        # Access the weather_icon API
        response = client.get('/api/weather_icon?cityName=Sydney&date=2024-03-20')
        assert response.status_code == 200
   #graph.py is currently being worked on so this test isn't complete     
"""
def test_graph(client, app):
   with client:
      response = client.get('/graph')
      assert response.status_code == 302
   """