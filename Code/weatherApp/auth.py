import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_bcrypt import Bcrypt
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')
bcrypt = Bcrypt()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        datb = db.get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                datb.execute(
                    "INSERT INTO User (email, password) VALUES (?, ?)",
                    (email, hashed_password),
                )
                datb.commit()
            except datb.IntegrityError:
                error = f"User with email {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('/register.html')

#route to login page
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        datb = db.get_db()
        error = None
        user = datb.execute(
            'SELECT * FROM User WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['userId']  # Assuming userId is the correct column name
            return redirect(url_for('index'))

        flash(error)

    return render_template('/login.html')


#bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested. 
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
#logout of session
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#Checks if a user is loaded and redirects to the login page otherwise. 
#If a user is loaded the original view is called and continues normally.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

