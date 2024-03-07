# -------------------------------------------------
# test_factory.py
'''
Unit tests for the app factory create_app
'''
'''
Starter Code sources:
- [Flask docs tutorial: Test Coverage](https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/) (newer commits)
'''
# -------------------------------------------------
from weatherApp import create_app

#test_config is the only behaviour that can change; that's why we test it
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing