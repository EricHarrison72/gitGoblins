# --------------------------------------------------
# test_auth.py
'''
Unit tests for user registration.
'''
'''
Start code sources:
- https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/#authentication
'''
# --------------------------------------------------

import bcrypt
from flask import session
from weatherApp.db import get_db
from weatherApp import predictions
from tests.auth_actions import (
    register_and_login_test_user,
    register_test_user,
    login_test_user,
    logout_test_user
)

# =====================================================
# REGISTRATION TESTS
# -----------------
def test_register__normal(client, app):
    assert client.get('/auth/register').status == '200 OK'

    correct_redirect_location = "/auth/login"
    registration_response = register_test_user(client)
    assert registration_response.location == correct_redirect_location

    with app.app_context():
        user_that_should_exist = get_db().execute(
            "SELECT * FROM user WHERE email = 'test@gmail.com'",
        ).fetchone()
    
    assert user_that_should_exist is not None

def test_register__duplicate_email(client):
    register_test_user(client, email='test@gmail.com')
    duplicate_email_response = register_test_user(client, email='test@gmail.com')
    expected_error_message = b'User with email test@gmail.com is already registered.'

    assert expected_error_message in duplicate_email_response.data

def test_register__no_email(client):
    no_email_response = register_test_user(client, email='')
    expected_error_message = b'Email is required.'
    
    assert expected_error_message in no_email_response.data

def test_register__no_password(client):
    no_password_response = register_test_user(client, password='')
    expected_error_message = b'Password is required.'

    assert expected_error_message in no_password_response.data

# LOGIN TESTS
# -----------
def test_login__normal(client, app):

    # Make sure app has a prediction model so loading '/' doesn't fail
    with app.app_context():
        predictions.train_and_save_model()

    register_test_user(client)
    login_response = login_test_user(client)
    correct_redirect_location = '/'

    assert login_response.location == correct_redirect_location

    # Ensure that logged in user can actually navigate the website
    with client:
        index_response = client.get('/')
        assert index_response.status == '200 OK'

def test_login__missing_or_incorrect_email(client):
    expected_error_message = b'Incorrect email.'

    no_email_response = login_test_user(client, email='')
    assert expected_error_message in no_email_response.data

    incorrect_email_response = login_test_user(client)
    assert expected_error_message in incorrect_email_response.data

def test_login__incorrect_password(client):
    register_test_user(client, password='correctpassword')
    incorrect_password_response = login_test_user(client, password='wrongpassword')
    expected_error_message = b'Incorrect password.'

    assert expected_error_message in incorrect_password_response.data

# LOGOUT TESTS
# ------------
def test_logout(client):
    register_and_login_test_user(client)
    with client:
        logout_test_user(client)
        assert 'user_id' not in session

# ===========================================================
# ADMIN AUTHENTICATION TESTS
# ---------------------------
def test_passcode(client, app):
    assert client.get('/auth/passcode').status == '200 OK'

    # Test with correct passcode
    with client.session_transaction() as session:
        session['passcode'] = '12'
    response = client.post('/auth/passcode', data={'passcode': '12'})
    assert response.headers["Location"] == "/auth/admin_register"

    # Check if 'passcode' is in session after successful verification
    with client.session_transaction() as session:
        assert 'passcode' in session
        
#register admin test
def test_admin_register(client, app):
    # Ensure that the admin register page redirects to the login page due to missing passcode
    response = client.get('/auth/admin_register', follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid passcode' in response.data
    
    # Test admin registration with valid passcode but missing email
    with client.session_transaction() as session:
        session['passcode'] = '12'
    response_missing_email = client.post(
        '/auth/admin_register',

        data={
            'email': '',  # Missing email
            'password': 'admin123',
            'city_id': '1'  # Provide a valid city ID
        }
    )

    # Test admin registration with valid passcode and all required data
    with client.session_transaction() as session:
        session['passcode'] = '12'
    response_valid_registration = client.post(
        '/auth/admin_register',

        data={
            'email': 'admin@test.com',
            'password': 'admin123',
            'city_id': '1'  # Provide a valid city ID
        }

    )
    # Check if it redirects to the login page
    assert response_valid_registration.headers["Location"] == "/auth/login"
    
    # Verify that the admin user is successfully registered in the database
    with app.app_context():
        assert get_db().execute(
             "SELECT * FROM user WHERE email = 'admin@test.com'",
        ).fetchone() is not None


# Combined test for admin registration, dashboard access, and admin route
def test_admin_register_dashboard_and_admin_route(client, app):
    # 1. Enter the passcode
    with client.session_transaction() as session:
        session['passcode'] = '12'
    response_passcode = client.post('/auth/passcode', data={'passcode': '12'})
    assert response_passcode.status_code == 302  # Redirect status code

    # 2. Register an admin account
    response_register = client.post(
        '/auth/admin_register',
        data={
            'email': 'admin@example.com',
            'password': 'admin_password',
            'city_id': '1'  # Provide a valid city ID
        }
    )
    assert response_register.status_code == 302  # Redirect status code

    # 3. Log in as admin
    response_login = client.post('/auth/login', data={'email': 'admin@example.com', 'password': 'admin_password'})
    assert response_login.status_code == 302  # Redirect status code

    # 4. Access the admin dashboard
    response_dashboard = client.get('/auth/admin_dashboard')
    assert response_dashboard.status_code == 200  # Successful access status code
    # Optionally, add assertions to check the content of the dashboard page if needed

    # 5. Simulate submitting a form to update weather data (access admin route)
    response_update_weather = client.post('/admin', data={'cityName': '1', 'tempMin': '10', 'tempMax': '20', 'date': '2014-04-01'})
    assert response_update_weather.status_code == 400  # Redirect status code

