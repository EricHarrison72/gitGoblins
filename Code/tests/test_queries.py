# ---------------------------------------------------
# test_queries.py
'''
Contains unit tests for queries.py
'''
# --------------------------------------------------
import pytest
from weatherApp.queries import get_weather_data

@pytest.fixture()
def expected_dict_1():
    return {
        'city_name': 'Albany', 
        'date': '2008-12-01', 
        'temp_high': 22.9, 
        'temp_low': 13.4, 
        'rainfall': 0.6, 
        'raining': False, 
        'wind_speed': 44, 
        'wind_dir': 'W'
    }


def test_get_weather_data(app, expected_dict_1):
    # 1 test when parameters are passed and data exists for those parameters
    with app.app_context():
        assert expected_dict_1 == get_weather_data('Albany', '2008-12-01')


    # 2 test parameters passed and no data exists
    # 3 test no parameters passed