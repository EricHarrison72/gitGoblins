# -------------------------------------------------
# auth_actions.py
'''
Contains functions related to the authentication of
test users. Note that cityIds must be in the test db.
99 = Springfield, 100 = Shelbyville

The reason these are in their own module instead
of being connected to a fixture object is because there
were problems with the client and auth contexts not
matching.
'''
'''
Starter Code sources:
- [Flask Docs: Testing - Authentication](https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/#authentication)
'''
# -------------------------------------------------
DEFAULT_NEW_USER_ID = 3 # (because in most contexts we only register one new user, and there are two users in test db by default)

def register_and_login_test_user(client):
    '''
    Note: Default cityId is 99 for Springfield (in test db only).
    '''
    register_test_user(client)
    login_test_user(client)

def register_test_user(client, email='test@gmail.com', password='test', cityId='99'):
    '''
    Note: Default cityId is 99 for Springfield (in test db only).
    '''
    return client.post(
        '/auth/register',
        data = {
            'email': email,
            'password': password,
            'city_id': cityId 
        })

def login_test_user(client, email='test@gmail.com', password='test'):
    return client.post(
        '/auth/login',
        data = {
            'email': email,
            'password': password
        })

def logout_test_user(client):
    return client.get('/auth/logout')