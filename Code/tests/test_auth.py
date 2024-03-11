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

@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('', '', b'Email is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, email, password, message):
    response = client.post(
        '/auth/register',
        data={'email': email, 'password': password}
    )
    assert message.decode('utf-8') in response.get_data(as_text=True)

    
 #The tests for the login view are very similar to those for register. 
 #Rather than testing the data in the database, 
 # session should have user_id set after logging in.   
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()

    assert response.headers.get("Location") == "/"
    
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['email'] == 'test@gmail.com'


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('a', 'test', b'Incorrect email.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.get_data(as_text=True).encode('utf-8')

    
#Testing logout is the opposite of login. 
#session should not contain user_id after logging out.

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
