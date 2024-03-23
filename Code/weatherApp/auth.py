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

        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                datb.execute(
                    "INSERT INTO User (email, password, firstName, lastName, emailList) VALUES (?, ?, ?, ?, ?)",
                    (email, hashed_password, first_name, last_name, email_list)
                )
                datb.commit()
                flash("Registration successful. You can now log in.")
                return redirect(url_for("auth.login"))
            except datb.IntegrityError:
                error = f"User with email {email} is already registered."

        flash(error)

    return render_template('auth/register.html.jinja')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        datb = db.get_db()
        error = None
        
        user = datb.execute(
            'SELECT userId, password, isAdmin FROM User WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not bcrypt.check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['userId']
            if user['isAdmin']:
                return redirect(url_for('auth.admin_dashboard'))
            else:
                return redirect(url_for('views.weather_summary'))

        flash(error)

    return render_template('auth/login.html.jinja')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            'SELECT * FROM User WHERE userId = ?', (user_id,)
        ).fetchone()


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@auth_bp.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    passcode = session.get('passcode')
    if passcode != '12':
        flash('Invalid passcode')
        return redirect(url_for('auth.login'))

    datb = db.get_db()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        email_list = bool(request.form.get('email_list'))

        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                datb.execute(
                    "INSERT INTO User (email, password, firstName, lastName, emailList, isAdmin) VALUES (?, ?, ?, ?, ?, ?)",
                    (email, hashed_password, first_name, last_name, email_list, True)
                )
                datb.commit()
                flash("Admin registration successful.")
                return redirect(url_for("auth.login"))
            except datb.IntegrityError:
                error = f"User with email {email} is already registered."

        flash(error)

    return render_template('auth/admin_register.html.jinja')


@auth_bp.route('/passcode', methods=['GET', 'POST'])
def passcode():
    if request.method == 'POST':
        entered_answer = request.form['passcode']

        if entered_answer == '12':
            session['passcode'] = entered_answer
            return redirect(url_for('auth.admin_login'))

        flash('Incorrect answer')

    return render_template('auth/passcode.html.jinja')


@auth_bp.route('/admin_login', methods=('GET', 'POST'))
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        datb = db.get_db()
        error = None
        
        user = datb.execute(
            'SELECT userId, password FROM User WHERE email = ? ', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not bcrypt.check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['userId']

            # Update isAdmin to true for the logged-in user
            datb.execute(
                'UPDATE User SET isAdmin = 1 WHERE userId = ?', (user['userId'],)
            )
            datb.commit()

            return redirect(url_for('auth.admin_dashboard'))

        flash(error)

    return render_template('auth/admin_login.html.jinja')


@auth_bp.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = db.get_db().execute(
        'SELECT isAdmin FROM User WHERE userId = ?', (user_id,)
    ).fetchone()

    if user is None or not user['isAdmin']:
        return redirect(url_for('auth.login'))

    return render_template('admin_dashboard.html.jinja')
