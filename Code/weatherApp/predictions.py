# --------------------------------------------------
# predictions.py
'''
Contains the python code required to build a machine learning
model to predict rainfall for a specific city and date
'''
'''
Start Code sources:
- [Random Forest Classification with Scikit-Learn](https://www.datacamp.com/tutorial/random-forests-classifier-python)
'''
# --------------------------------------------------

#Project Data
from . import db
import sqlite3

# Data Processing
import pandas as pd
import joblib

# Modelling
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

# Query data from database into a pandas dataframe to be used in the model
def create_dataframe(datb):
    query = "SELECT * FROM WeatherInstance"
    df_weather = pd.read_sql_query(query, datb)
    
    return df_weather

def process_data(df):
    # Fill missing numeric values with 0
    # Note: Some of these are missing because the cities don't have
    # data for them, this may mess up the prediction accuracy
    
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

    # Convert 'rainToday' from boolean to int (0 or 1)
    df['rainToday'] = df['rainToday'].map({'Yes': 1, 'No': 0, 'NA': 0}).astype(int)
    # Convert 'rainTomorrow' from boolean to int (0 or 1)
    df['rainTomorrow'] = df['rainTomorrow'].map({'Yes': 1, 'No': 0, 'NA': 0}).astype(int)
    
    # Use hot encoding to convert catigorical data into numerical data
    df = pd.get_dummies(df, columns=['windGustDir', 'windDir9am', 'windDir3pm'])
    
    return df

def build_model(df):
    #Split data into training and testing data
    X = df.drop(['rainTomorrow', 'cityId', 'date'], axis=1)  # Exclude non-feature columns
    y = df['rainTomorrow'] # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    
    # Initialize the model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    rf_model.fit(X_train, y_train)

    # Make predictions
    y_pred = rf_model.predict(X_test)
    
    # Print scores of model upon initialization
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1 Score:", f1_score(y_test, y_pred))
    
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
    X = df_input.drop(['rainTomorrow', 'cityId', 'date'], axis=1, errors='ignore')  # errors='ignore' helps avoid errors if these columns aren't present
    
    # Ensure all expected columns are present
    expected_features = model.feature_names_in_  # This attribute holds the feature names used during fit
    for feature in expected_features:
        if feature not in X.columns:
            X[feature] = 0  # Add missing columns filled with default value (e.g., 0)
    
    # Reorder columns to match the training data
    X = X[expected_features]
    
    # Make the prediction
    prediction = model.predict(X)
    
    # Returns 1 if it predicts rain, and 0 if it doesn't predict rain
    # This prediction is for the day AFTER the `date` used
    return prediction[0]

# Helper function to create model and convert cityName into cityId
def predict_rain(city_name, date):
    # Load the model that's saved when running init_db_command
    rf_model = joblib.load('rainfall_prediction_model.pkl')
    
    # Returns 1 if it predicts rain, and 0 if it doesn't predict rain
    return _predict_rain_(city_name, date, rf_model)


# This function creates and saves the prediction model, it is only called when running init_db_command
def train_and_save_model():
    datb = db.get_db()

    # Create prediction model
    df_weather = create_dataframe(datb)
    df_processed = process_data(df_weather)
    rf_model = build_model(df_processed)
    
    # Save the model to disk
    joblib.dump(rf_model, 'rainfall_prediction_model.pkl')
    
    print("Model trained and saved successfully.")
