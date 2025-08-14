from backend.test.conftest import client, admin_account_factory


def test_login_user(client, admin_account_factory):
    """
    GIVEN a user register in the database
    WHEN the user send the login request to the endpoint of auth/login
    THEN The login is successful and a token is returned
    """

    admin_account_factory()

    payload = {
        "email": "test_account@email.com",
        "password": "12345678",
    }

    response = client.post('/auth/login', json=payload)

    assert response.status_code == 200
    data = response.get_json()


