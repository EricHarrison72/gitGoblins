import unittest
from unittest.mock import MagicMock, patch
from flask import Flask

from weatherApp.admin import admin_bp


class TestAdminBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(admin_bp)
        self.client = self.app.test_client()

    @patch('weatherApp.admin.db.get_db')
    def test_admin_endpoint(self, mock_get_db):
        mock_cursor = MagicMock()
        mock_fetchone = MagicMock(return_value=('CityName',))
        mock_cursor.fetchone = mock_fetchone
        mock_datb = MagicMock()
        mock_datb.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_datb

        with self.app.test_request_context('/admin', method='POST',
                                           data={'city_id': '1', 'tempMin': '10.0', 'tempMax': '20.0', 'date': '2024-03-29'}):
            response = self.client.post('/admin')

            # Ensure that the database methods are called with the correct parameters
            mock_datb.execute.assert_called_once_with('''
                UPDATE WeatherInstance
                SET tempMin = ?, tempMax = ?
                WHERE cityId = ? AND date = ?
            ''', ('10.0', '20.0', '1', '2024-03-29'))
            mock_datb.commit.assert_called_once()

        # Verify that the response status code is 302
        self.assertEqual(response.status_code, 302)
        mock_get_db.assert_called_once()
        mock_datb.execute.assert_called_once()  # Assertion corrected here
        mock_fetchone.assert_called_once()
        mock_datb.commit.assert_called_once()

    def test_admin_endpoint_invalid_input(self):
        with self.app.test_request_context('/admin', method='POST',
                                       data={'city_id': '1', 'tempMin': 'abc', 'tempMax': '20.0', 'date': '2024-03-29'}):
            response = self.client.post('/admin')
            self.assertEqual(response.status_code, 400 if 'Invalid input value' in response.json.get('error', '') else 500)


    @patch('weatherApp.admin.db.get_db')
    def test_admin_endpoint_error(self, mock_get_db):
        mock_datb = MagicMock()
        mock_datb.execute.side_effect = Exception("Mocked exception")
        mock_get_db.return_value = mock_datb

        with self.app.test_request_context('/admin', method='POST',
                                           data={'city_id': '1', 'tempMin': '10.0', 'tempMax': '20.0', 'date': '2024-03-29'}):
            response = self.client.post('/admin')
            self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
