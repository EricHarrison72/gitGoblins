from flask import Blueprint, g, redirect, render_template, request, url_for
from . import db
set_bp = Blueprint('settings', __name__)

@set_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Get form data
        email_list = request.form.get('emailList') == 'on'  # Checkbox value
        city_id = int(request.form.get('cityId'))

        # Update user settings in the database
        try:
            user_id = g.user['userId']  # Get user ID from g.user
            db.update_user_settings(user_id,  email_list, city_id)
            # Redirect to index after successful update
            return redirect(url_for('views.index'))
        except Exception as e:
            error_message = 'An error occurred while updating user settings: {}'.format(str(e))
            return render_template('error.html', error_message=error_message)

    # If method is GET, render the settings page
    # You need to pass user data and city data to the template
    user_id = g.user['userId']  # Get user ID from g.user
    user = db.get_user_settings(user_id)  # Get user data from database
    cities = db.get_cities()  # Get city data from database

    return render_template('settings.html.jinja', user=user, cities=cities)
