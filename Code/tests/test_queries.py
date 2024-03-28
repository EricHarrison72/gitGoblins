# ---------------------------------------------------
# test_queries.py
'''
Contains unit tests for queries.py
'''
# --------------------------------------------------
import pytest
from weatherApp.queries import (
    get_weather_data,
    #get_temp_in_range,
    add_space
)

# --------
# FIXTURES

@pytest.fixture()
def expected_weather_dict():
    return {
         # (data that I know is in test DB)
        'params passed, data exists': {
            'city_name': 'Springfield',
            'date': '2023-01-01',
            'temp_high': 10.0,
            'temp_low': -5.0,
            'rainfall': 0.0,
            'raining': 'No',
            'wind_speed': 30,
            'wind_dir': 'N',
            'cloud': 3
        },
         # (There is no data for Albury in the test DB)
        'params passed, no data exists': {
             'city_name': 'NO DATA for Albury on this date',
            'date': '2007-12-01',
            'temp_high': 0,
            'temp_low': 0,
            'rainfall': 0.0,
            'raining': '?',
            'wind_speed': 0,
            'wind_dir': '?',
            'cloud': 0
        },
        '`None` params passed': {
            'city_name': 'NO DATA',
            'date': 'No Date',
            'temp_high': 0,
            'temp_low': 0,
            'rainfall': 0.0,
            'raining': '?',
            'wind_speed': 0,
            'wind_dir': '?',
            'cloud': 0
        }
    }


# Note
'''
Since sqlite queries return Sqlite3.Row objects that are hard to mock,
it makes the most sense to make the expected tables dictionaries and
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

def test_get_weather_data(app, expected_weather_dict):

    with app.app_context():
        assert (expected_weather_dict['params passed, data exists']
                == get_weather_data('Springfield', '2023-01-01'))

        assert (expected_weather_dict['params passed, no data exists']
                == get_weather_data('Albury', '2007-12-01'))

        assert (expected_weather_dict['`None` params passed']
                == get_weather_data(None, None))

def test_add_space():
      assert add_space('AliceSprings') == 'Alice Springs'
      assert add_space('NewYorkCity') == 'New York City'

# def test_get_temp_in_range(app, expected_temp_table):
    
#     with app.app_context():
#         real_temp_table = get_temp_in_range('Springfield', '2023-01-01', '2023-01-03')

#     for i in range(len(expected_temp_table)):
#         for key in expected_temp_table[i].keys():
#             assert expected_temp_table[i][key] == real_temp_table[i][key]

# --------

