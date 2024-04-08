# ---------------------------------------------------
# test_predictions.py
'''
Contains unit tests for predictions.py
'''
# --------------------------------------------------

# Mocking/testing imports
from unittest.mock import patch, MagicMock
from sklearn.exceptions import UndefinedMetricWarning
import warnings

# Dataframe and modelling imports
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Function imports
from weatherApp.db import get_db
from weatherApp.predictions import (
    create_dataframe,
    process_data,
    build_model,
    predict_rain,
    train_and_save_model
)


def test_create_dataframe(app):
    # Expected contents from the test database data.sql
    expected_columns = [
    'cityId', 'date', 'tempMin', 'tempMax', 'sunshine', 'rainfall',
    'evaporation', 'cloud9am', 'cloud3pm', 'pressure9am', 'pressure3pm',
    'humidity9am', 'humidity3pm', 'windGustSpeed', 'windGustDir',
    'windSpeed9am', 'windSpeed3pm', 'windDir9am', 'windDir3pm', 
    'rainToday', 'rainTomorrow'
    ]
    expected_rows = [
        (    99, '2017-01-01',    0.0,    9.0,         4,      0.0,         4.5,        1,        3,      1013.5,      1010.5,          80,          50,            12,         'W',           10,           20,        'N',        'S',      'No',        'Yes'),
        (    99, '2023-01-01',   -5.0,    10.0,        8,      0.0,         4.5,        1,        3,      1013.5,      1010.5,          80,          50,            12,         'W',           10,           20,        'N',        'S',      'No',        'Yes'),
        (    99, '2023-01-02',   -3.0,    'NA',        4,      5.0,         3.0,        1,        3,      1013.5,      1010.5,          80,          50,            35,       'NNE',           10,           20,        'N',        'S',     'Yes',        'Yes'),
        (    99, '2023-01-03',   'NA',    30.0,        1,     'NA',         0.1,        1,        3,      1013.5,      1010.5,          80,          50,           123,        'SW',           10,           20,        'N',        'S',     'Yes',         'No'),
        (   100, '2023-01-02',    0.0,    15.0,       10,      0.0,         5.0,        0,        1,      1015.0,      1012.0,          70,          40,            25,         'E',            5,           15,        'E',        'W',      'No',        'Yes')
    ]
    
    # Run create_dataframe with test database
    with app.app_context():
        datb = get_db()
        df = create_dataframe(datb)
        
    # Assertions to verify the dataframe content and structure
    assert not df.empty, "The DataFrame should not be empty"
    # Check the DataFrame structure
    assert list(df.columns) == expected_columns, "DataFrame columns do not match the expected structure"
    # Check the number of rows
    assert len(df) == len(expected_rows), "DataFrame does not contain the expected number of rows"


def test_process_data():
    # Sample data setup, including None and 'NA' value to ensure all edge cases are covered
    data = {
    'cityId': [101, 102, 103, 104],
    'date': ['2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08'],
    'tempMin': [-1.0, None, 2.5, 'NA'],
    'tempMax': ['15.0', 20.5, None, '22.0'],
    'sunshine': [10, None, 5, 8], 
    'rainfall': ['0.0', 1.5, 'NA', None],  
    'evaporation': [5.2, None, 2.7, 'NA'], 
    'cloud9am': [1, 3, None, 0],
    'cloud3pm': [2, None, 3, 4], 
    'pressure9am': [1013.5, '1012.0', None, 'NA'],
    'pressure3pm': ['1011.5', 1010.0, 'NA', None],
    'humidity9am': [80, None, 60, 70],
    'humidity3pm': [50, 55, None, 45],
    'windGustSpeed': [25, None, 30, 20],
    'windGustDir': ['N', 'S', None, 'E'],
    'windSpeed9am': [10, 5, None, 15],
    'windSpeed3pm': [20, 25, None, 10],
    'windDir9am': ['N', 'S', None, 'E'],
    'windDir3pm': ['E', 'W', None, 'S'], 
    'rainToday': ['Yes', 'No', None, 'Yes'], 
    'rainTomorrow': ['No', 'Yes', 'No', None] 
    }
    df = pd.DataFrame(data)
    
    # Process the data
    processed_df = process_data(df)
    
    # Assertions
    # Check that numeric cols are filled properly
    assert not processed_df[['sunshine', 'rainfall', 'evaporation', 'cloud9am']].isnull().any().any(), "Numeric columns should not contain any null values"
    
    # Check the conversion of 'rainToday' and 'rainTomorrow' to int
    assert all(processed_df['rainToday'].isin([0, 1])), "'rainToday' should contain only 0s and 1s"
    assert all(processed_df['rainTomorrow'].isin([0, 1])), "'rainTomorrow' should contain only 0s and 1s"
    
    # Check that 'windGustDir' and other categorical columns are filled with 'unknown' for missing values
    assert not processed_df['windGustDir_unknown'].isnull().any(), "Categorical columns should have 'unknown' for missing values"
    
    # Check that the temperature columns are filled with median values where applicable
    assert processed_df['tempMin'].isnull().sum() == 0, "'tempMin' should have no null values"
    assert processed_df['tempMax'].isnull().sum() == 0, "'tempMax' should have no null values"
    
    # Ensure that one-hot encoding was applied to categorical columns
    assert 'windGustDir_N' in processed_df.columns and 'windDir9am_N' in processed_df.columns, "One-hot encoding should create new columns for categorical values"
    
def test_build_model():
    # Create a mock DataFrame
    data = {
        'cityId': [1, 2, 3, 4, 5, 6],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06'],
        'feature1': [5, 6, 7, 8, 9, 10],
        'feature2': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        'rainToday': [0, 1, 0, 1, 0, 1],
        'rainTomorrow': [1, 0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)

    # Call build_model function
    model = build_model(df)

    # Check if the model is an instance of the expected class
    assert isinstance(model, RandomForestClassifier), "Model is not an instance of RandomForestClassifier"
    
    # Optionally, you can check if the model has attributes that would indicate it has been trained
    assert hasattr(model, "feature_importances_"), "Model does not seem to be trained"

# It's hard to test this function properly as the model is too complex to test
# So this test just ensures that there are no errors thrown, and it returns either 0 or 1 for a known city/date
def test_predict_rain_integration(app):
    with app.app_context():
        city_name = 'Springfield'
        date = '2023-01-01'
        
        prediction = predict_rain(city_name, date)
        assert prediction in [0, 1], "Prediction should be 0 or 1"
        
        city_name = 'Springfield'
        date = '2027-01-01'
        
        prediction = predict_rain(city_name, date)
        assert prediction == 'Error', "Prediction should be Error"
        

# Using patch to mock specific functions used in the test_and_save function
# This test doesn't really test much, it just ensures the function makes it to the end and helps with coverage
@patch('weatherApp.predictions.joblib.dump')
@patch('weatherApp.predictions.create_dataframe')
@patch('weatherApp.db.get_db') 
def test_train_and_save_model(mock_get_db, mock_create_dataframe, mock_joblib_dump):
    # Suppress warnings for this function, as it's throwing warnings due to the predictions having no True Positives
    # and we don't care about the functionality of the model in this test
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UndefinedMetricWarning)
        # Define a mock DataFrame that includes all columns expected by process_data
        data = {
        'cityId': [101, 102, 103, 104],
        'date': ['2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08'],
        'tempMin': [-1.0, None, 2.5, 'NA'],
        'tempMax': ['15.0', 20.5, None, '22.0'],
        'sunshine': [10, None, 5, 8], 
        'rainfall': ['0.0', 1.5, 'NA', None],  
        'evaporation': [5.2, None, 2.7, 'NA'], 
        'cloud9am': [1, 3, None, 0],
        'cloud3pm': [2, None, 3, 4], 
        'pressure9am': [1013.5, '1012.0', None, 'NA'],
        'pressure3pm': ['1011.5', 1010.0, 'NA', None],
        'humidity9am': [80, None, 60, 70],
        'humidity3pm': [50, 55, None, 45],
        'windGustSpeed': [25, None, 30, 20],
        'windGustDir': ['N', 'S', None, 'E'],
        'windSpeed9am': [10, 5, None, 15],
        'windSpeed3pm': [20, 25, None, 10],
        'windDir9am': ['N', 'S', None, 'E'],
        'windDir3pm': ['E', 'W', None, 'S'], 
        'rainToday': ['Yes', 'No', None, 'Yes'], 
        'rainTomorrow': ['No', 'Yes', 'No', None] 
        }
        mock_df = pd.DataFrame(data)

        # Configure mock_create_dataframe to return the mock DataFrame
        mock_create_dataframe.return_value = mock_df

        # Mock db.get_db() to do nothing or return a dummy value as needed
        mock_get_db.return_value = MagicMock()

        # Call the function under test
        train_and_save_model()

        # Assert that joblib.dump was called once, indicating the model was saved
        mock_joblib_dump.assert_called_once()