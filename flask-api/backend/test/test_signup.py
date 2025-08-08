import json
from backend.test.conftest import client, db_session
from backend.repositories.user_repository import UserRepository

def test_sign_up_user(client, db_session):
    payload = {
        "name": "Samuel",
        "last_name": "Jauregui",
        "email": "samjaursz@gmail.com",
        "password": "123456",
        "password_confirmation": "123456",
        "status": True
    }

    response = client.post('/auth/sign_up', json=payload)

    print("Status code:", response.status_code)
    print("Response JSON:", response.get_json())

    assert response.status_code == 200
    json_data = response.get_json()
    assert "error" not in json_data