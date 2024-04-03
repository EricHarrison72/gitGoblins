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
    get_template,
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

# Expected template for High Temperature
@pytest.fixture()
def expected_template_1():
    return """
<!DOCTYPE html>
<html lang="en">
<html>
    <body>
        <h1>Weather alert for Springfield.</h1>
      	<br>
      	<p>
          Hello, you are receiving this alert because Springfield is expecting high temperatures.
      	</p>
     	 <p>
      	  Expect a temperature high of 10&deg;C.
      	</p>
    </body>
</html>"""

# Expected Template for Low Temperature
@pytest.fixture()
def expected_template_2():
    return '''
<!DOCTYPE html>
<html lang="en">
<html>
    <body>
        <h1>Weather alert for Springfield.</h1>
      	<br>
      	<p>
          Hello, you are receiving this alert because Springfield is expecting low temperatures.
      	</p>
     	<p>
      	  Expect a temperature low of -5&deg;C.
      	</p>
    </body>
</html>'''

# Expected Template for High Winds
@pytest.fixture()
def expected_template_3():
    return '''
<!DOCTYPE html>
<html lang="en">
<html>
    <body>
        <h1>Weather alert for Springfield.</h1>
      	<br>
      	<p>
          Hello, you are receiving this alert because Springfield is expecting high wind speeds and gusts.
      	</p>
     	 <p>
      	  Expect wind speeds up to 30km/h.
      	</p>
    </body>
</html>'''

# Expected Template for Rain
@pytest.fixture()
def expected_template_4():
    return '''
<!DOCTYPE html>
<html lang="en">
<html>
    <body>
        <h1>Weather alert for Springfield.</h1>
      	<br>
      	<p>
          Hello, you are receiving this alert because Springfield is expecting rain.
      	</p>
     	 <p>
      	  Expect 0mm of rain.
      	</p>
    </body>
</html>'''

# -------------------
# TESTS
#--------------------

# Test for send_email, tests that a message is sent and that the subject line is correct
def test_send_email(app, test_to, test_subject, test_template):
    with app.app_context():
        with mail.record_messages() as outbox:
            send_email(test_to, test_subject, test_template)
            assert len(outbox) == 1
            assert outbox[0].subject == "Weather Alert for Canberra"

# Test for get_template, tests that the template returned is what is expected
def test_get_template(app, expected_template_1, expected_template_2, expected_template_3, expected_template_4):
     
    # defining some dictionaries to pass into the function
    test_dict_1 = {
        "city_name": "Springfield",
        "date": "2023-01-01",
        "data_point": "HighTemperature"
    }

    test_dict_2 = {
        "city_name": "Springfield",
        "date": "2023-01-01",
        "data_point": "LowTemperature"
    }

    test_dict_3 = {
        "city_name": "Springfield",
        "date": "2023-01-01",
        "data_point": "Wind"
    }

    test_dict_4 = {
        "city_name": "Springfield",
        "date": "2023-01-01",
        "data_point": "Rain"
    }

    # Checks that each data point is correctly obtained from the database and that each corresponding template is grabbed
    with app.app_context():
          template = get_template(test_dict_1)
          assert expected_template_1 == template

          template = get_template(test_dict_2)
          assert expected_template_2 == template

          template = get_template(test_dict_3)
          assert expected_template_3 == template

          template = get_template(test_dict_4)
          assert expected_template_4 == template