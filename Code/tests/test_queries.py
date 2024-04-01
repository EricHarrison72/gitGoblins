# ---------------------------------------------------
# test_queries.py
'''
Contains unit tests for queries.py
'''
# --------------------------------------------------
import pytest
from weatherApp.queries import (
    get_weather_data,
    get_temp_in_range,
    _add_space
)

# --------
# FIXTURES
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
            'rain_today': 'No', 
            'wind_speed': 30, 
            'wind_dir': 'N',
            'cloud_3pm': 3,
            'sunshine': 8,
            'evaporation': 4.5,
            'cloud_9am': 1,
            'pressure_9am': 1013.5,
            'pressure_3pm': 1010.5,
            'humidity_9am': 80,
            'humidity_3pm': 50,
            'wind_speed_9am': 10,
            'wind_speed_3pm': 20,
            'wind_dir_9am': 'N',
            'wind_dir_3pm': 'S',
            'rain_tomorrow': 'No'
        }

# Expected dict for: params passed, no data exists
@pytest.fixture()
def expected_dict_2():
        # There is no data for Albury in the test DB
        return {
            'city_name': 'NO DATA for Albury on this date', 
            'date': '2007-12-01', 
            'temp_low': 0,
            'temp_high': 0,
            'sunshine': 0,
            'rainfall': 0.0,
            'evaporation': 0.0,
            'cloud_9am': 0,
            'cloud_3pm': 0,
            'pressure_9am': 0.0,
            'pressure_3pm': 0.0,
            'humidity_9am': 0,
            'humidity_3pm': 0,
            'wind_speed': 0,
            'wind_dir': '?',
            'wind_speed_9am': 0,
            'wind_speed_3pm': 0,
            'wind_dir_9am': '?',
            'wind_dir_3pm': '?',
            'rain_today': '?',
            'rain_tomorrow': '?'
        }

# Expected dict for: 'None' params passed
@pytest.fixture()
def expected_dict_3():
        return {
            'city_name': 'NO DATA',
            'date': 'No Date',
            'temp_low': 0,
            'temp_high': 0,
            'sunshine': 0,
            'rainfall': 0.0,
            'evaporation': 0.0,
            'cloud_9am': 0,
            'cloud_3pm': 0,
            'pressure_9am': 0.0,
            'pressure_3pm': 0.0,
            'humidity_9am': 0,
            'humidity_3pm': 0,
            'wind_speed': 0,
            'wind_dir': '?',
            'wind_speed_9am': 0,
            'wind_speed_3pm': 0,
            'wind_dir_9am': '?',
            'wind_dir_3pm': '?',
            'rain_today': '?',
            'rain_tomorrow': '?'
        }

# Note
'''
Since sqlite queries return Sqlite3.Row objects that are hard to mock,
it make the most sence to make the expected tables dictionaries and
to then iterate over each item in both the expected dictionary and real
row, testing equality for each pair of items instead of for the whole object.
'''
@pytest.fixture()
def expected_temp_table():
     return [
          {'date':'2023-01-01', 'temp_low': -5.0, 'temp_high' : 10.0},
          {'date':'2023-01-02', 'temp_low': -3.0, 'temp_high' : 20.0},
          {'date':'2023-01-03', 'temp_low': -2.0, 'temp_high' : 30.0}
     ]

# --------
# TESTS

def test_get_weather_data(app, expected_dict_1, expected_dict_2, expected_dict_3):

    with app.app_context():
        # params passed, data exists
        assert expected_dict_1 == get_weather_data('Springfield', '2023-01-01')

        # params passed, no data exists
        assert expected_dict_2 == get_weather_data('Albury', '2007-12-01')

        #'None' params passed
        assert expected_dict_3 == get_weather_data(None, None)

def test_add_space():
      assert _add_space('AliceSprings') == 'Alice Springs'
      assert _add_space('NewYorkCity') == 'New York City'

def test_get_temp_in_range(app, expected_temp_table):
    
    with app.app_context():
        real_temp_table = get_temp_in_range('Springfield', '2023-01-01', '2023-01-03')

    for i in range(len(expected_temp_table)):
        for key in expected_temp_table[i].keys():
            assert expected_temp_table[i][key] == real_temp_table[i][key]

# --------

