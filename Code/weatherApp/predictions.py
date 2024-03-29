# --------------------------------------------------
# predictions.py
'''
Contains the python code required to build a machine learning
model to predict rainfall for a specific city and date.
The model makes its prediction based on all the available 
weather data for that city/date.
'''
'''
Start Code sources:
- [Random Forest Classification with Scikit-Learn](https://www.datacamp.com/tutorial/random-forests-classifier-python)
'''
# --------------------------------------------------

import warnings

#Project Data
from . import db

# Data Processing
import pandas as pd
import joblib

# Modelling
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split


def create_dataframe(datb):
    '''
    Query data from database into a pandas dataframe to be used in the model
    '''
    query = "SELECT * FROM WeatherInstance"
    df_weather = pd.read_sql_query(query, datb)
    
    return df_weather

def process_data(df):
    '''
    - Convert most of the data to numeric types
    - replace missing numeric values with 0
      - Note: Some of these are missing because the cities don't have
        data for them, this may mess up the prediction accuracy
    '''
    # Convert non-numeric to NaN and fill missing numeric values
    numeric_cols = ['sunshine', 'rainfall', 'evaporation', 'cloud9am', 'cloud3pm', 'pressure9am', 'pressure9am', 'pressure3pm', 'humidity9am', 'humidity3pm', 'windGustSpeed', 'windSpeed9am', 'windSpeed3pm', 'tempMin', 'tempMax']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Handle non-numeric entries
        if col in ['tempMin', 'tempMax']:
            # Fill with median for temperature columns
            df[col] = df[col].fillna(df[col].median())
        else:
            # Fill other numeric columns with 0
            df.loc[:, col] = df.loc[:, col].fillna(0)

    # For categorical data, you might fill missing values with the mode or a placeholder value
    categorical_cols = ['windGustDir', 'windDir9am', 'windDir3pm']
    for col in categorical_cols:
        df.loc[:, col] = df[col].fillna('unknown')

    # Ignore FutureWarnings that this code produces when running the test
    # We can safely ignore the warnings as the dataset does not use None for missing values, it uses 'NA'
    # and the warning is only being thrown about problems from this conversion in the future for None type values
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        
        # Convert 'rainToday' and 'rainTomorrow' to numeric, replacing 'Yes', 'No', 'NA', and handling None values
        df['rainToday'] = df['rainToday'].replace({'Yes': 1, 'No': 0, 'NA': 0, None: 0}).fillna(0).astype(int)
        df['rainTomorrow'] = df['rainTomorrow'].replace({'Yes': 1, 'No': 0, 'NA': 0, None: 0}).fillna(0).astype(int)
    
    # Use hot encoding to convert catigorical data into numerical data
    df = pd.get_dummies(df, columns=['windGustDir', 'windDir9am', 'windDir3pm'])
    
    return df

def build_model(df):
    #Split data into training and testing data
    input_vars = df.drop(['rainTomorrow', 'cityId', 'date'], axis=1)  # Exclude non-feature columns
    target_var = df['rainTomorrow']

    input_train, input_test, target_train, target_test = train_test_split(input_vars, target_var, test_size=0.2, random_state=42)
    
    # Initialize the model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    rf_model.fit(input_train, target_train)

    # Make predictions
    target_pred = rf_model.predict(input_test)
    
    # Print scores of model upon initialization
    print("Accuracy:", accuracy_score(target_test, target_pred))
    print("Precision:", precision_score(target_test, target_pred))
    print("Recall:", recall_score(target_test, target_pred))
    print("F1 Score:", f1_score(target_test, target_pred))
    
    return rf_model


def _predict_rain_(city_name, date, model):
    datb = db.get_db()
    
    # Retrieve cityId for the given cityName
    city_id_query = "SELECT cityId FROM City WHERE cityName = ?"
    cur = datb.cursor() 
    cur.execute(city_id_query, (city_name,))
    city_id_result = cur.fetchone()
    
    if city_id_result is None:
        return None
    
    city_id = city_id_result[0]  # Extract cityId from the query result
    
    # Process data for specific date and city to prepare it for the model
    query = f"SELECT * FROM WeatherInstance WHERE cityId = {city_id} AND date = '{date}'"
    df_input = process_data(pd.read_sql_query(query, datb))
    
    # Ensure cursor and database connections are closed after use
    cur.close()
    
    # Drop colums that aren't in prediction model
    prediction_input = df_input.drop(['rainTomorrow', 'cityId', 'date'], axis=1, errors='ignore')  # errors='ignore' helps avoid errors if these columns aren't present
    
    # Ensure all expected columns are present
    expected_features = model.feature_names_in_  # This attribute holds the feature names used during fit
    for feature in expected_features:
        if feature not in prediction_input.columns:
            prediction_input[feature] = 0  # Add missing columns filled with default value (e.g., 0)
    
    # Reorder columns to match the training data
    prediction_input = prediction_input[expected_features]
    
    # Make the prediction
    prediction = model.predict(prediction_input)
    
    # Returns 1 if it predicts rain, and 0 if it doesn't predict rain
    # This prediction is for the day AFTER the `date` used
    return prediction[0]


def predict_rain(city_name, date):
    '''
    (Helper function) to create model and convert cityName into cityId
    '''
    # Load the model that's saved when running init_db_command
    rf_model = joblib.load('rainfall_prediction_model.pkl')
    
    # Returns 1 if it predicts rain, and 0 if it doesn't predict rain
    return _predict_rain_(city_name, date, rf_model)


def train_and_save_model():
    '''
    This function creates and saves the prediction model, 
    it is only called when running `init_db_command` in `db.py`
    '''
    datb = db.get_db()

    # Create prediction model
    df_weather = create_dataframe(datb)
    df_processed = process_data(df_weather)
    rf_model = build_model(df_processed)
    
    # Save the model to disk
    joblib.dump(rf_model, 'rainfall_prediction_model.pkl')
    
    print("Model trained and saved successfully.")
