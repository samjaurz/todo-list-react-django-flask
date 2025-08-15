from backend.test.conftest import client, token_factory

def test_read_user(client, token_factory):
    """
    GIVEN a token
    WHEN the uses/Task decode teh token validate the user exists
    THEN Return list of task
    """

    data_retrieved = token_factory()

    user_id = data_retrieved["info"]["user_id"]
    client.set_cookie(
        'access_token',
        value=data_retrieved["access_token"],
        samesite='None',
        httponly=True,
        secure=True,
        max_age=3600,
    )
    response = client.get(f'/users/{user_id}')

    assert response.status_code == 200
    data = response.get_json()
    print(data)
