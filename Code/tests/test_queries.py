# ---------------------------------------------------
# test_queries.py
'''
Contains unit tests for queries.py
'''
# --------------------------------------------------
import pytest
from weatherApp.queries import get_weather_data

'''
Note: I had to split these dicts into 3 separate fixtures because the old fixture
built incorrectly on GitHub Actions, causing integration tests to fail
'''

# Expected dict for: params passed, data exists
@pytest.fixture()
def expected_dict_1():
    # data that I know is in test DB
    return {
            'city_name': 'Springfield', 
            'date': '2023-01-01', 
            'temp_high': 10.0, 
            'temp_low': -5.0, 
            'rainfall': 0.0, 
            'raining': 'No', 
            'wind_speed': 30, 
            'wind_dir': 'N'
        }

# Expected dict for: params passed, no data exists
@pytest.fixture()
def expected_dict_2():
        # There is no data for Albury in the test DB
        return {
            'city_name': 'NO DATA for Albury on this date', 
            'date': '2007-12-01', 
            'temp_high': 0, 
            'temp_low': 0, 
            'rainfall': 0.0, 
            'raining': '?', 
            'wind_speed': 0, 
            'wind_dir': '?'
        }

# Expected dict for: 'None' params passed
@pytest.fixture()
def expected_dict_3():
        return {
            'city_name': 'NO DATA', 
            'date': 'No Date', 
            'temp_high': 0, 
            'temp_low': 0, 
            'rainfall': 0.0, 
            'raining': '?', 
            'wind_speed': 0, 
            'wind_dir': '?'
        }

def test_get_weather_data(app, expected_dict_1, expected_dict_2, expected_dict_3):

    with app.app_context():
        # params passed, data exists
        assert expected_dict_1 == get_weather_data('Springfield', '2023-01-01')

        # params passed, no data exists
        assert expected_dict_2 == get_weather_data('Albury', '2007-12-01')

        #'None' params passed
        assert expected_dict_3 == get_weather_data(None, None)