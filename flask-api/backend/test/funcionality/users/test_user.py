from backend.test.conftest import client


def test_read_user(client, gen_token):
    """
    GIVEN an authenticated user ( user_id, token )
    WHEN a GET request is made to the /users endpoint + user_id
    THEN return status code is 200 and validate the correct user information
    """

    user_id = gen_token["user"]["id"]
    client.set_cookie(
        "refresh_token",
        value=gen_token["tokens"]["refresh_token"],
        samesite="None",
        httponly=True,
        secure=True,
    )
    response = client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {gen_token['tokens']['access_token']}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert data["id"] == user_id
    assert data["name"] == "test"
    assert data["last_name"] == "account"
    assert data["email"] == "test_account@email.com"
    assert data["status"] == True


def test_get_all_task_by_user(client, gen_token, task_factory):
    """
    GIVEN an authenticated user ( user_id, token )
    WHEN a GET request is made to the /users/tasks
    THEN return status code is 200 with an array of tasks
    """

    user_id = gen_token["user"]["id"]
    task_factory()
    task_factory()
    task_factory()
    client.set_cookie(
        "refresh_token",
        value=gen_token["tokens"]["refresh_token"],
        samesite="None",
        httponly=True,
        secure=True,
    )
    response = client.get(
        f"/users/{user_id}/tasks",
        headers={"Authorization": f"Bearer {gen_token['tokens']['access_token']}"},
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["user_id"] == user_id
    assert len(data["tasks"]) == 3
    assert data["tasks"][0]["name"] == "test_task"
    assert data["tasks"][0]["status"] == False


def test_search_all_task_by_user(client, gen_token, task_factory):
    """
    GIVEN an authenticated user ( user_id, token )
    WHEN a GET request is made to the /users/<id_user>/search
    THEN return status code is 200 with all the tasks found
    """

    user_id = gen_token["user"]["id"]
    task_factory()
    task_factory()
    task_factory()

    client.set_cookie(
        "refresh_token",
        value=gen_token["tokens"]["refresh_token"],
        samesite="None",
        httponly=True,
        secure=True,
    )

    response = client.get(
        f"users/{user_id}/search/?name=Tas",
        headers={"Authorization": f"Bearer {gen_token['tokens']['access_token']}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["tasks"][0]["name"] == "test_task"
