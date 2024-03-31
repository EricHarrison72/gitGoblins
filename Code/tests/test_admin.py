import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from weatherApp.admin import admin_bp

class TestAdminBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(admin_bp)
        self.client = self.app.test_client()

    # @patch('weatherApp.admin.db.get_db')
    # def test_admin_endpoint(self, mock_get_db):
    #     # Mock database cursor
    #     mock_cursor = MagicMock()
    #
    #     # Send a POST request to admin endpoint
    #     with self.app.test_request_context('/admin', method='POST',
    #                                        data={'city_id': '1', 'tempMin': '10', 'tempMax': '20', 'date': '2024-03-29'}):
    #         response = self.client.post('/admin')
    #
    #         # Verify get_db is called
    #         mock_get_db.assert_called_once()
    #
    #         # Get the return value of get_db
    #         mock_datb = mock_get_db.return_value
    #
    #         # Assert that execute method is called once with the expected SQL query and parameters
    #         mock_datb.execute.assert_called_once_with(
    #             '''
    #             UPDATE WeatherInstance
    #             SET tempMin = ?, tempMax = ?
    #             WHERE cityId = ? AND date = ?
    #             ''',
    #             ('10', '20', '1', '2024-03-29')
    #         )
    #
    #         # Verify the response status code is 302 (redirect)
    #         self.assertEqual(response.status_code, 302)
    #
    #         # Reset the call count for further assertions
    #         mock_datb.execute.reset_mock()

    def test_admin_endpoint_invalid_input(self):
        # Send a POST request with invalid input to admin endpoint
        with self.app.test_request_context('/admin', method='POST',
                                           data={'city_id': '1', 'tempMin': 'abc', 'tempMax': '20.0', 'date': '2024-03-29'}):
            response = self.client.post('/admin')
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
