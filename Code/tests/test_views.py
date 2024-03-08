# ------------------------------------------------
# test_weatherApp.py
'''
I created this file as part of a flask testing tutorial.
In the future we will create several test files. (see test_example)
'''
'''
Starter Code sources:
- [Getting Started With Testing in Flask](https://www.youtube.com/watch?v=RLKW7ZMJOf4)
'''
# ------------------------------------------------

# Example of a test that uses the client fixture
def test_home(client):
    response = client.get("/")

    # check that the page has something we know is going to be there
    assert b"<title>Home</title>" in response.data

def test_weather_summary():

    assert 1