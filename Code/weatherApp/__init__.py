# ------------------------------------------------------
# __init__.py in weatherApp
'''
This file initializes the app package ('weatherApp').
Most importantly, it contains the app factory ('create_app()'),
which creates an instance of the app with a database, 
and loads the data from weatherAUS.csv into the database.

This is run automatically when you run the app using the terminal command:
`flask --app weatherApp --debug run`
'''
'''
Starter code sources:
- [Flask docs tutorial - Application Setup] (https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/)
- [Flask docs tutorial - Define and Access the Database](https://flask.palletsprojects.com/en/3.0.x/tutorial/database/)
'''
#--------------------------------------------------------
from flask import Flask, render_template, url_for
import os, csv, sqlite3
from flask_bcrypt import Bcrypt
#Initalizes database and returns app with working db
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'weatherApp.sqlite'),
    )
    if test_config is None:
        # Load configuration from 'instance/config.py'
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    
    
    # Initialize Flask-Bcrypt with the app instance
    bcrypt = Bcrypt(app)
    
    # Import and register the database commands from db.py
    from . import db
    db.init_app(app)
    
    # Import and register blueprints
    from .views import bp as app_blueprint
    app.register_blueprint(app_blueprint)
    
    #Import and register the blueprint from the factory using app.register_blueprint().
    from . import auth
    app.register_blueprint(auth.bp)
    
    
    
    return app