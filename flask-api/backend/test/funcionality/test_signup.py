from backend.test.conftest import client, app

def test_sign_up_user(client):
    """
        GIVEN field of user data for registration
        WHEN the user send the request to the endpoint of auth/sign_up
        THEN the user is created successfully and validate the response data
    """
    payload = {
        "name": "Samuel",
        "last_name": "Jauregui",
        "email": "samjaursz@gmail.com",
        "password": "123456",
        "password_confirmation": "123456",
        "status": True
    }

    response = client.post('/auth/sign_up', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "access_token" in data
    assert data["message"] == "Password is valid! User authenticated."




