from backend.test.conftest import client, app

def test_login_user(client, admin_account_factory, app):
    admin_account_factory()

    payload = {
        "email": "test_account@email.com",
        "password": "12345678",
    }

    response = client.post('/auth/login', json=payload)

    print("Parsed JSON:", response.get_json())
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data




