# ---------------------------------------------------
# test_queries.py
'''
Contains unit tests for queries.py
'''
# --------------------------------------------------
import pytest
from weatherApp.queries import (
    get_user_city,
    get_weather_data,
    get_data_in_range,
    _generate_column_script,
    add_space
)
# ==================================
# SMALLER TESTS
# -------------
def test_add_space():
      assert add_space('AliceSprings') == 'Alice Springs'
      assert add_space('NewYorkCity') == 'New York City'

def test_generate_column_script(app):
    expected_column_script_A = 'Column1,Column2,Column3'
    assert (_generate_column_script(['Column1', 'Column2', 'Column3'])
            == expected_column_script_A)
    
    expected_column_script_B = 'Column1,Column4'
    assert (_generate_column_script(['Column1', 'Column4'])
            == expected_column_script_B)
    
# =======================================
# get_user_city TEST
#--------------------------
def test_get_user_city(client, app):
    register_and_login(client)
    with app.test_request_context():
        user_id = 3 # (because we only registered 1 extra user in this context)
        assert get_user_city(user_id) == 'Springfield'

# helper
def register_and_login(client):
    client.post('/auth/register', data={
        'email': 'test@gmail.com',
        'password': 'a',
        'city_id': '99'  # for Springfield
    })
    client.post('/auth/login', data={
        'email': 'test@gmail.com',
        'password': 'a'
    })

# ======================================
# get_weather_data FIXTURES
# -------------------------
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
            'rain_today': 'No', 
            'wind_speed': 12, 
            'wind_dir': 'W',
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
            'rain_tomorrow': 'Yes'
        },
        # (There is no data for Albury in the test DB)
        'params passed, no data exists': {
            'city_name': 'NO DATA for Albury', 
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
        },
        '`None` params passed': {
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
    }

# get_weather_data TESTS
# ----------------------
def test_get_weather_data(app, expected_weather_dict):

    with app.app_context():
        assert (expected_weather_dict['params passed, data exists']
                == get_weather_data('Springfield', '2023-01-01'))

        assert (expected_weather_dict['params passed, no data exists']
                == get_weather_data('Albury', '2007-12-01'))

        assert (expected_weather_dict['`None` params passed']
                == get_weather_data(None, None))

# =======================================
# TODO
'''
nontesting:
- handle incorrect date range error (in query and graphs)

testing:
- for multiple columns (temp), for one column (rain):
    - 1. with valid city and dates - check return vals -- MOST IMPORTANT
    - 2. without valid city and dates - check error response
- for invalid column - check error response? maybe
'''
# get_data_in_range FIXTURES
# -------------------------
class ValidInfo:
    def __init__(
        self,
        city_and_dates,
        multiple_cols,
        single_col,
        expected_mult_col_table,
        expected_single_col_table
    ):
        self.city_and_dates = city_and_dates 
        self.multiple_cols = multiple_cols
        self.single_col = single_col
        self.expected_mult_col_table = expected_mult_col_table
        self.expected_single_col_table = expected_single_col_table

@pytest.fixture()
def valid_info():
    multiple_cols = ['tempMin', 'tempMax']
    single_col = ['rainfall']

    city_and_dates = {
        'city_name': 'Springfield',
        'start_date': '2023-01-01',
        'end_date': '2023-01-03'
    }
    expected_mult_col_table = [
        {'date':'2023-01-01', 'tempMin': -5.0, 'tempMax' : 10.0},
        {'date':'2023-01-02', 'tempMin': -3.0, 'tempMax' : 'NA'},
        {'date':'2023-01-03', 'tempMin': 'NA', 'tempMax' : 30.0}
    ]
    expected_single_col_table= [
        {'date':'2023-01-01', 'rainfall': 0.0},
        {'date':'2023-01-02', 'rainfall': 5.0},
        {'date':'2023-01-03', 'rainfall': 'NA'}
    ]

    return ValidInfo(
        city_and_dates,
        multiple_cols,
        single_col,
        expected_mult_col_table,
        expected_single_col_table
    )

# get_data_in_range TESTS
#------------------------
def test_get_data_in_range__valid_query(app, valid_info):

    with app.app_context():
        real_mult_col_table = get_data_in_range(valid_info.multiple_cols, valid_info.city_and_dates)
        real_single_col_table = get_data_in_range(valid_info.single_col, valid_info.city_and_dates)

    num_rows = len( valid_info.expected_mult_col_table)

    for row in range(num_rows):
        for key in valid_info.expected_mult_col_table [row].keys():
            assert (
                valid_info.expected_mult_col_table [row][key]
                == real_mult_col_table [row][key]
            )

        for key in valid_info.expected_single_col_table [row].keys():
            assert (
                valid_info.expected_single_col_table [row][key]
                == real_single_col_table [row][key]
            )

def test_get_data_in_range__invalid_query(app):
    '''
    Test not yet implemented because responding to invalid queries is not
    yet part of get_data_in_range (this is a TDD reminder to do that tho).
    '''
    pass
