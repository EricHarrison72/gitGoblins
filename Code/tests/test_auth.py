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


#The register view should render successfully on GET. On POST with valid form data, 
# it should redirect to the login URL and the user’s data should be in the database.
def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    
    # Test registering user
    response = client.post(
        '/auth/register',
        data={
            'email': 'test@gmail.com',
            'password': 'a',
            'city_id': '1'  # Provide a valid city_id in the form data
        }
    )
    
    # Check if it redirects to login page
    assert response.headers["Location"] == "/auth/login"
    
    # Test registering user with duplicate email
    response_duplicate_email = client.post(
        '/auth/register',
        data={
            'email': 'test@gmail.com',
            'password': 'a',
            'city_id': '1'  # Provide a valid city_id in the form data
        }
    )
    
    # Check if it redirects to login page
    assert b'User with email test@gmail.com is already registered.' in response_duplicate_email.data

    # Test register with no email
    response_no_email = client.post(
        '/auth/register',
        data={'email': '', 'password': 'a', 'city_id': '1'}  # Provide a valid city_id
    )
    
    # Check for correct error message
    assert b'Email is required.' in response_no_email.data

    # Test register with no password
    response_no_password = client.post(
        '/auth/register',
        data={'email': 'test@gmail.com', 'password': '', 'city_id': '1'}  # Provide a valid city_id
    )
    
    # Check for correct error message
    assert b'Password is required.' in response_no_password.data

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

        # Insert a city record with cityId 1 (assuming it exists in your database)
        db.execute(
            "INSERT INTO City (cityId, cityName) VALUES (?, ?)",
            (1, 'Example City')
        )
        db.commit()

        # Assign the user (ID 100) to cityId 1
        db.execute(
            "UPDATE User SET cityId = ? WHERE userId = ?",
            (1, 100)
        )
        db.commit()
    # Test login with no email
    response_no_email = client.post(
        '/auth/login', data={'email': '', 'password': 'a'}
    )
    # Check for correct error message
    assert b'Incorrect email.' in response_no_email.data
    
    # Test login with incorrect password
    response_no_password = client.post(
        '/auth/login', data={'email': 'test_user@gmail.com', 'password': 'wrongpassword'}
    )
    # Check for correct error message
    assert b'Incorrect password.' in response_no_password.data
    # Test login with user ID 100
    response = client.post(
        '/auth/login',
        data={'email': 'test_user@gmail.com', 'password': 'password'}
    )
    # Check if it redirects to the home page
    assert response.headers["Location"] == "/"

    # Check if user ID 100 is stored in session
    with client:
        response_index = client.get('/')
        assert response_index.status_code == 200  # Ensure the request is successful
       

        # Print debugging information
        print(response_index.data)  # Print the response content


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
   

       
       
