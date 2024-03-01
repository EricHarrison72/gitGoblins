from flask import Flask

import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from 'instance/config.py'
    app.config.from_pyfile('config.py', silent=True)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import and register the database commands from db.py
    from . import db
    db.init_app(app)

    # Import and register your blueprints
    from . import app as app_blueprint
    app.register_blueprint(app_blueprint.bp)

    return app
