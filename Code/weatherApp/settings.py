# settings.py

from . import db

def update_user_settings(user_id, first_name, last_name, email, email_list, password, city_id):
    """
    Update user settings in the database.
    
    Args:
    - user_id: ID of the user to update settings for
    - first_name: New first name
    - last_name: New last name
    - email: New email
    - email_list: Whether the user wants to be on an email list (True or False)
    - password: New password
    - city_id: ID of the new city
    
    Returns:
    - True if the update was successful, False otherwise
    """
    try:
        datb = db.get_db()
        datb.execute('''
            UPDATE Users
            SET firstName = ?, lastName = ?, email = ?, emailList = ?, password = ?, cityId = ?
            WHERE userId = ?
        ''', (first_name, last_name, email, email_list, password, city_id, user_id))
        datb.commit()
        return True
    except Exception as e:
        print("Error updating user settings:", str(e))
        return False
