# ------------------------------------------------
# test_views.py
'''
This currently exists to test (mostly front end stuff) in views.py
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
   assert b"<title>" in response.data


# this test doesn't do much, but it forces the CI pipeline to try to access the /weather_summary page
# def test_weather_summary(client):
#     response = client.get("/weather_summary")

#     assert b"<title>Weather Summary</title>" in response.data