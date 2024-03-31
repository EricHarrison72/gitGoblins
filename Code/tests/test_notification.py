# ---------------------------------------------------
# test_notification.py
'''
Contains unit tests for notification.py
'''
# --------------------------------------------------

import pytest

# Imports for testing
from weatherApp.notification import (
    send_email,
    mail
)

# Creating fixtures for testing
@pytest.fixture()
def test_subject():
    return "Canberra"

@pytest.fixture()
def test_to():
    return ['gitgoblins4@gmail.com']

@pytest.fixture()
def test_template():
    return ""
    
# Test for send_email, tests that a message is sent and that the subject line is correct
def test_send_email(app, test_to, test_subject, test_template):
    with app.app_context():
        with mail.record_messages() as outbox:
            send_email(test_to, test_subject, test_template)
            assert len(outbox) == 1
            assert outbox[0].subject == "Weather Alert for Canberra"
        
