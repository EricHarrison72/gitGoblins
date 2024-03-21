# --------------------------------------------------
# test_weather.py
'''
Unit tests for user registration.
'''
# --------------------------------------------------

# Import necessary modules for testing
import pytest
from flask import session

# Import map module
from weatherApp.weather import determine_icon_based_on_weather

@pytest.fixture()
def expected_error():
    #Data that should return error icon
    return {
            'city_name': 'Albury', 
            'date': '2023-01-01', 
            'temp_high': 0.0, 
            'temp_low': 0.0, 
            'rainfall': 0.0, 
            'raining': 'No', 
            'wind_speed': 30, 
            'wind_dir': 'N',
            'cloud': 3
        }
    
@pytest.fixture()
def expected_rain():
    #Data that should return rain icon
    return {
            'city_name': 'Albury', 
            'date': '2023-01-01', 
            'temp_high': 10.0, 
            'temp_low': 2.0, 
            'rainfall': 0.0, 
            'raining': 'Yes', 
            'wind_speed': 30, 
            'wind_dir': 'N',
            'cloud': 3
        }

@pytest.fixture()
def expected_wind():
    #Data that should return wind icon
    return {
            'city_name': 'Albury', 
            'date': '2023-01-01', 
            'temp_high': 10.0, 
            'temp_low': 2.0, 
            'rainfall': 0.0, 
            'raining': 'No', 
            'wind_speed': 81, 
            'wind_dir': 'N',
            'cloud': 3
        }

@pytest.fixture()
def expected_cloud():
    #Data that should return cloud icon
    return {
            'city_name': 'Albury', 
            'date': '2023-01-01', 
            'temp_high': 10.0, 
            'temp_low': 2.0, 
            'rainfall': 0.0, 
            'raining': 'No', 
            'wind_speed': 30, 
            'wind_dir': 'N',
            'cloud': 5
        }
    
@pytest.fixture()
def expected_partcloud():
    #Data that should return partcloud icon
    return {
            'city_name': 'Albury', 
            'date': '2023-01-01', 
            'temp_high': 10.0, 
            'temp_low': 2.0, 
            'rainfall': 0.0, 
            'raining': 'No', 
            'wind_speed': 30, 
            'wind_dir': 'N',
            'cloud': 3
        }
    
@pytest.fixture()
def expected_sun():
    #Data that should return sun icon
    return {
            'city_name': 'Albury', 
            'date': '2023-01-01', 
            'temp_high': 10.0, 
            'temp_low': 2.0, 
            'rainfall': 0.0, 
            'raining': 'No', 
            'wind_speed': 30, 
            'wind_dir': 'N',
            'cloud': 0
        }
    
@pytest.fixture()
def expected_value_error():
    #Data that should return sun icon
    return {
            'city_name': 'Albury', 
            'date': '2023-01-01', 
            'temp_high': 10.0, 
            'temp_low': 2.0, 
            'rainfall': 0.0, 
            'raining': 'No', 
            'wind_speed': 'NA', 
            'wind_dir': 'N',
            'cloud': 0
        }
    
def test_determine_icon_based_on_weather(app, expected_error, expected_rain, expected_wind, expected_cloud, expected_partcloud, expected_sun, expected_value_error):

    with app.app_context():
        # data for error returns error
        assert 'error' == determine_icon_based_on_weather(expected_error)

        # data for rain returns rain
        assert 'rain' == determine_icon_based_on_weather(expected_rain)

        # data for wind returns wind
        assert 'wind' == determine_icon_based_on_weather(expected_wind)
        
        # data for cloud returns cloud
        assert 'cloud' == determine_icon_based_on_weather(expected_cloud)
        
        # data for partclloud returns partcloud
        assert 'partcloud' == determine_icon_based_on_weather(expected_partcloud)
        
        # data for sun returns sun
        assert 'sun' == determine_icon_based_on_weather(expected_sun)
        
        # data with non-number wind speed results in valueError (ignoring wind) and returns sun
        assert 'sun' == determine_icon_based_on_weather(expected_value_error)