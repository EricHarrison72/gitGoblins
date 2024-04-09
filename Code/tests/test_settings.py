# ---------------------------------------------------
# test_queries.py
'''
Contains unit tests for queries.py
'''
# --------------------------------------------------
from tests import auth_actions


def test_update_user_settings__authenticated(client):
    with client:
        auth_actions.register_and_login_test_user(client)

        # Update user settings
        response = client.post('/settings', data={
            'emailList': 'on',
            'cityId': '2'  
        })

        assert response.status_code == 302 
        
