# ------------------------------------------------------
# db.py
'''
Methods for creating, accessing and tearing down the 
database using the specs in schema.sql.
'''
# ------------------------------------------------------
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

#Returns current database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

#Closes current database
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#Initializes database to app using schema.sql
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#Used for initializing database via command line, I couldn't make it work properly - Eric
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

#Used to initialized database commands
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
