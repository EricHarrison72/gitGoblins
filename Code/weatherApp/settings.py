# ------------------------------------------------
# settings.py
'''
Views and logic for updating user settings.
'''
# -------------------------------------------------
from flask import Blueprint, g, redirect, render_template, request, url_for
from .auth import login_required
from . import db

set_bp = Blueprint('settings', __name__)

@set_bp.route('/settings', methods=['GET', 'POST'])
@login_required  
def settings():
    if request.method == 'POST':
        email_list = request.form.get('emailList') == 'on' 
        city_id = int(request.form.get('cityId'))

        # Update user settings in the database
        user_id = g.user['userId']  
        db.update_user_settings(user_id,  email_list, city_id)
       
        return redirect(url_for('views.index'))

    # Pass user data and city data to the template
    user_id = g.user['userId'] 
    user = db.get_user_settings(user_id)  
    cities = db.get_cities()  

    return render_template('settings.html.jinja', user=user, cities=cities)
