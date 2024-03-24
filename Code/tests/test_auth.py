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
import pytest
from flask import g, session
from weatherApp import create_app
from weatherApp.db import get_db, init_db


#The register view should render successfully on GET. On POST with valid form data, 
# it should redirect to the login URL and the user’s data should be in the database.
def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'email': 'test@gmail.com', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE email = 'test@gmail.com'",
        ).fetchone() is not None


def test_login(client, app):
    # Manually insert user with ID 100 into the database with hashed password
    with app.app_context():
        db = get_db()
        hashed_password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.execute(
            "INSERT INTO user (userId, email, password) VALUES (?, ?, ?)",
            (100, 'test_user@gmail.com', hashed_password)
        )
        db.commit()

    # Test login with user ID 100
    response = client.post(
        '/auth/login',
        data={'email': 'test_user@gmail.com', 'password': 'password'}
    )
    # Check if it redirects to the weather summary page
    assert response.headers["Location"] == "/weather_summary"

    # Check if user ID 100 is stored in session
    with client:
        client.get('/')
        assert session['user_id'] == 100


def test_logout(client, app):
    # Manually insert user with ID 100 into the database with hashed password
    with app.app_context():
        db = get_db()
        hashed_password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.execute(
            "INSERT INTO user (userId, email, password) VALUES (?, ?, ?)",
            (100, 'test_user@gmail.com', hashed_password)
        )
        db.commit()

    # Test login with user ID 100
    client.post(
        '/auth/login',
        data={'email': 'test_user@gmail.com', 'password': 'password'}
    )

    # Test logout with user ID 100 within client context
    with client:
        client.get('/auth/logout')
        # Ensure that the user ID is removed from the session
        assert 'user_id' not in session

# Test passcode verification
def test_passcode(client, app):
    assert client.get('/auth/passcode').status_code == 200

    # Test with correct passcode
    with client.session_transaction() as session:
        session['passcode'] = '12'
    response = client.post('/auth/passcode', data={'passcode': '12'})
    assert response.headers["Location"] == "/auth/admin_login"

    # Check if 'passcode' is in session after successful verification
    with client.session_transaction() as session:
        assert 'passcode' in session
        
#register admin test
def test_register_admin(client, app):
    # Ensure that the registration page loads successfully
    assert client.get('/auth/register').status_code == 200
    
    # Register a new admin user with valid form data
    response = client.post(
        '/auth/register', 
        data={'email': 'admin@test.com', 'password': 'admin123', 'isAdmin': True}
    )
    
    # Check if the registration redirects to the login page
    assert response.headers["Location"] == "/auth/login"

    # Verify that the admin user is successfully registered in the database
    with app.app_context():
        assert get_db().execute(
             "SELECT * FROM user WHERE email = 'admin@test.com'",
        ).fetchone() is not None
        
        
def test_admin_login_redirect(client):
    # Access the admin login page
    response = client.get('/auth/admin_login')
    assert response.status_code == 200

    # Simulate a successful admin login
    response = client.post('/auth/admin_login', data={'email': 'admin@example.com', 'password': 'admin123'})
    assert response.status_code == 200  # Check if it redirects
    assert response.location == 'http://localhost/admin_dashboard'  # Check if it redirects to the update page
