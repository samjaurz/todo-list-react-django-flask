from backend.test.conftest import client


def test_verification_user(client, gen_token, db_session):
    """
    GIVEN an authorized token and data for make the tasks
    WHEN the token is validated the tasks is created with the data
    THEN return a status code 201 and a json object with the tasks data
    """

    user_email = gen_token["user"]["email"]
    payload = {
        "email": user_email,
    }
    response = client.post("/auth/resend_email_verification", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    print(data)
