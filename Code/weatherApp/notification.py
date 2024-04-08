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
from . import mail, queries
from flask_mail import Message
from flask import current_app, render_template

def send_email(to, city, template):
    '''
    - sends an email notification to recipients in a list of emails "to", with the subject header of "Weather Alert for (subject)", using an HTML template of "template"
    '''

    email_subject = 'Weather Alert for ' + city

    msg = Message(
        subject = email_subject,
        recipients = to,
        html = template,
        sender = current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def get_template(data : dict):
    '''
    - returns a rendered template that corresponds to the event and data that is passed in
    - expects an event type as a string and the data parsed into a dictionary with
        - a city name as 'city_name'
        - a date as 'date'
        - wthe weather event as 'event_type'
    '''
    template = None
    date = data.get('date')
    event_type = data.get('event_type')

    event_type = event_type.replace(' ', '') # (just in case)

    city_dict = queries.get_weather_data(data['city_name'], date)

    if(len(city_dict.get('city_name')) > len(data.get('city_name'))):
        return template

    if event_type == 'HighTemperature':
        template = 'notif/email_high_temp.html.jinja'
        event_type = 'temp_high'
    elif event_type == 'LowTemperature':
        template = 'notif/email_low_temp.html.jinja'
        event_type = 'temp_low'
    elif event_type == 'Wind':
        template = 'notif/email_high_winds.html.jinja'
        event_type = 'wind_speed'
    elif event_type == 'Rain':
        template = 'notif/email_rain.html.jinja'
        event_type = 'rainfall'
        
    #data['data_point'] = queries.get_weather_data(data['city_name'], date).get(event_type)


    data['data_point'] = city_dict.get(event_type)


    return render_template(template, event_args = data)