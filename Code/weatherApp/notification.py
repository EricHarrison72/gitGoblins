# ------------------------------------------------------
# notification.py
'''
Code for the email notification system using FlaskMail
'''
'''
Resources used:
- [Educative, "How to send emails with API in Flask-Mail"](https://www.educative.io/answers/how-to-send-emails-with-api-in-flask-mail)
- [Flask-Mail Documentation](https://pythonhosted.org/Flask-Mail/)
'''
# ------------------------------------------

# import flask mail and current_app to get the proper app object
from . import mail
from flask_mail import Message
from flask import current_app

def send_email(to, subject, template):
    '''
    - sends an email notification to recipients in a list of emails "to", with the subject header of "Weather Alert for (subject)", using an HTML template of "template"
    '''
    msg = Message(
        "Weather Alert for" + subject,
        recipients = to,
        html = template,
        sender = current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)



