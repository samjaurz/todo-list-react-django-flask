import json
from backend.test.conftest import client, db_session
from backend.repositories.user_repository import UserRepository

def test_login_user(client, db_session):
    payload = {
        "email": "samjaursz@gmail.com",
        "password": "123456",
    }

    response = client.post('/auth/login', json=payload)

    json = f"{"Parsed JSON:", response.get_json()}"
    print(json)

