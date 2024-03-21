# -----------------------------------------------------
# auth.py
'''
Code establishes user authentication with registration, login, and logout routes, 
handling input validation and password hashing. 
It utilizes sessions to store user IDs upon successful login and 
includes a login_required decorator to ensure protected views are accessible only to authenticated users.
'''
'''
Starter code sources:
- https://flask.palletsprojects.com/en/3.0.x/tutorial/views/#login
'''
# -----------------------------------------------------

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_bcrypt import Bcrypt
from . import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
bcrypt = Bcrypt()


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    datb = db.get_db()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        email_list = bool(request.form.get('email_list'))

        # Get the last userId and increment it by 1
        last_user_id = get_last_user_id(datb)
        user_id = last_user_id + 1

        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                datb.execute(
                    "INSERT INTO User (userId, email, password, firstName, lastName, emailList) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, email, hashed_password, first_name, last_name, email_list)
                )
                datb.commit()
                flash("Registration successful. You can now log in.")
                return redirect(url_for("auth.login"))
            except datb.IntegrityError:
                error = f"User with email {email} is already registered."

        flash(error)

    return render_template('auth/register.html.jinja')


#route to login page
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        datb = db.get_db()
        error = None
        print(email)
        # Fetch user data including userId based on email
        user = datb.execute(
            'SELECT userId, password FROM User WHERE email = ?', (email,)
        ).fetchone()
       
        print(email)
        if user is None:
            error = 'Incorrect email.'
        elif not bcrypt.check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['userId']  # Store user ID in session
            
            return redirect(url_for('views.index'))

        flash(error)

    return render_template('auth/login.html.jinja')

@auth_bp.before_app_request
def load_logged_in_user():
    print(session)
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            'SELECT * FROM user WHERE userId = ?', (user_id,)
        ).fetchone()
        
#logout of session
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))

#Checks if a user is loaded and redirects to the login page otherwise. 
#If a user is loaded the original view is called and continues normally.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def get_last_user_id(datb):
    # Query the database to get the maximum userId
    result = datb.execute("SELECT MAX(userId) FROM User").fetchone()
    last_user_id = result[0] if result[0] is not None else 0
    return last_user_id
