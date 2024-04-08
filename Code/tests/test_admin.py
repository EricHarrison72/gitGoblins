def test_admin_get_request(client):
    """Test GET request to admin route."""
    response = client.get('/admin')
    # Assert based on expected GET behavior, e.g., status code or template used
    assert response.status_code == 200  # Example assertion

def test_admin_post_request_success(client):
    """Test successful POST request to admin route."""
    # Simulate POST request with valid data
    response = client.post('/admin', data={
        'city_id': '1',
        'tempMin': '10.5',
        'tempMax': '22.3',
        'date': '2024-04-01',
    })
    # Assert that the response is a redirect (status code 302) and redirects to the correct URL
    assert response.status_code == 302
    # Additional assertions can include checking if the database was updated correctly

def test_admin_post_request_invalid_data(client):
    """Test POST request with invalid data to admin route."""
    # Simulate POST request with invalid data, e.g., non-numeric city_id
    response = client.post('/admin', data={
        'city_id': 'invalid_id',
        'tempMin': 'not_a_number',
        'tempMax': '22.3',
        'date': '2024-04-01',
    })
    # Expect a 400 status code due to invalid input
    assert response.status_code == 400
    # You can also assert the specific error message if your API returns one