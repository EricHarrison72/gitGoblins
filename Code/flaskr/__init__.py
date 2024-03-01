#__innit__.py
from flask import Flask
from .db import init_db_command

import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['DATABASE'] = '/instance/database.db' #This isn't supposed to be necessary, but the next line wasn't working
    # Load configuration from 'instance/config.py'
    app.config.from_pyfile('config.py', silent=False)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    
    
    # Import and register the database commands from db.py
    from . import db
    db.init_app(app)

    print("Database commands imported.")
    
    #I couldn't figure out blueprints, maybe they'll help once I figure them out -Eric
    # Import and register your blueprints
    #from .views import bp as app_blueprint
    #app.register_blueprint(app_blueprint)
    
    # Initialize the database
    with app.app_context():
        db.init_db()
    
    return app
