# ---------------------------------------------------
# test_queries.py
'''
Contains unit tests for queries.py
'''
# --------------------------------------------------
import pytest
from weatherApp.queries import get_weather_data

@pytest.fixture()
def expected_dict():
    my_dict = {
        # data directly from the csv
        'params passed + data exists': {
            'city_name': 'Albury', 
            'date': '2008-12-01', 
            'temp_high': 22.9, 
            'temp_low': 13.4, 
            'rainfall': 0.6, 
            'raining': 'No', 
            'wind_speed': 44, 
            'wind_dir': 'W'
        },
        # data for Albury starts in 2008, so there should be no data for 2007
        'params passed + no data exists': {
            'city_name': 'NO DATA for Albury on this date', 
            'date': '2007-12-01', 
            'temp_high': 0, 
            'temp_low': 0, 
            'rainfall': 0.0, 
            'raining': '?', 
            'wind_speed': 0, 
            'wind_dir': '?'
        },
        'none params passed': {
            'city_name': 'NO DATA', 
            'date': 'No Date', 
            'temp_high': 0, 
            'temp_low': 0, 
            'rainfall': 0.0, 
            'raining': '?', 
            'wind_speed': 0, 
            'wind_dir': '?'
        }
    }

    return my_dict

def test_get_weather_data(app, expected_dict):
    
    with app.app_context():
        assert expected_dict['params passed + data exists'] == get_weather_data('Albury', '2008-12-01')
        assert expected_dict['params passed + no data exists'] == get_weather_data('Albury', '2007-12-01')
        assert expected_dict['none params passed'] == get_weather_data(None, None)