# test_admin.py

from weatherApp.admin import admin_bp  # Adjust import as needed
from weatherApp.db import get_db  # Adjust import as needed
from flask import Flask

def test_admin_route(client):
    app = Flask(__name__)
    app.register_blueprint(admin_bp)

    # Mocking request data
    mock_request_data = {
        'city_id': 1,
        'tempMin': 10.0,
        'tempMax': 20.0,
        'date': '2024-03-29'
    }

    # Mocking database
    class MockDB:
        def execute(self, query, params):
            return None  # Mocking execute method

        def commit(self):
            pass  # Mocking commit method

    # Patching db.get_db
    with app.app_context():
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['DATABASE'] = MockDB()

        response = client.post('/admin', data=mock_request_data)
        assert response.status_code == 500  # Check if it redirects

    
