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

# Example of a test that uses the client fixture
# TODO: current problem with this is that you need to be logged in to test these views
'''
def test_index(client):
   response = client.get("/")
   assert b"<header><h1>Home<h1><header>" in response.data
'''


# this test doesn't do much, but it forces the CI pipeline to try to access the /weather_summary page
# def test_weather_summary(client):
#     response = client.get("/weather_summary")

#     assert b"<title>Weather Summary</title>" in response.data

# Import necessary modules for testing
import pytest
from flask import session

# Import views module
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
