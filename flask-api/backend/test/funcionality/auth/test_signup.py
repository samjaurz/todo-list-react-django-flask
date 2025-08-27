from backend.test.conftest import client


def test_sign_up_user(client):
    """
    GIVEN field of user data for registration
    WHEN the user send the request to the endpoint of auth/sign_up
    THEN the user is created successfully and validate the response data
    """
    payload = {
        "name": "Test Name",
        "last_name": "Last Test ",
        "email": "test@gmail.com",
        "password": "123456",
        "password_confirmation": "123456",
        "status": False
    }

    response = client.post('/auth/sign_up', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Sign up successful"
    assert data["user_id"] is not None


def test_signup_user_already_exists(client, admin_user_factory):
    """
    GIVEN field of user data of user already in the database
    WHEN the user send the request to the endpoint of auth/sign_up
    THEN the sing up failed and return and error message
    """
    admin_user_factory()

    payload = {
        "name": "Test Name",
        "last_name": "Last Test ",
        "email": "test_account@email.com",
        "password": "123456",
        "password_confirmation": "123456",
        "status": False
    }

    response = client.post('/auth/sign_up', json=payload)
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Email already in use"


def test_signup_the_password_does_not_match(client, admin_user_factory):
    """
    GIVEN field of user data but the password and the password confirmation don't match
    WHEN the user send the request to the endpoint of auth/sign_up
    THEN the sing up failed because of the password does not match
    """
    payload = {
        "name": "Test Name",
        "last_name": "Last Test ",
        "email": "test_password_dont_match@gmail.com",
        "password": "password",
        "password_confirmation": "password_confirmation",
        "status": False
    }

    response = client.post('/auth/sign_up', json=payload)
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "password does not match"
