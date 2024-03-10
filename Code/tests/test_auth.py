import os
import tempfile
import pytest
from flask import Flask, session
from weatherApp import create_app, db

# Some basic test data
TEST_USER_EMAIL = 'test@example.com'
TEST_USER_PASSWORD = 'test_password'

@pytest.fixture
def app():
    # Create a temporary database for testing
    db_fd, db_path = tempfile.mkstemp()

    # Create the app with testing configuration
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test_secret_key',
    })

    # Establish a context for the app
    with app.app_context():
        db.init_db()

    yield app

    # Teardown: Close the database and remove the temporary file
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    # Create a test client for the app
    return app.test_client()

def test_register(client, app):
    # Ensure the register route behaves correctly

    # Test GET request
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data

    # Test POST request with valid data
    response = client.post('/auth/register', data={'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})
    assert response.status_code == 302  # Should redirect after successful registration

    # Test that user is registered in the database
    with app.app_context():
        user = db.get_db().execute("SELECT * FROM User WHERE email = ?", (TEST_USER_EMAIL,)).fetchone()
        assert user is not None
        assert user['email'] == TEST_USER_EMAIL

def test_login_logout(client, app):
    # Ensure the login and logout routes behave correctly

    # Test POST request with valid login data
    response = client.post('/auth/login', data={'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})
    assert response.status_code == 302  # Should redirect after successful login
    assert session['user_id'] is not None

    # Test GET request to check if the user is logged in
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Hello, ' + TEST_USER_EMAIL.encode('utf-8') in response.data

    # Test logout route
    response = client.get('/auth/logout')
    assert response.status_code == 302  # Should redirect after logout
    assert session.get('user_id') is None