from backend.test.conftest import client

def test_create_tasks(client, gen_token , task_factory):
    """
    GIVEN an authorized token and data for make the tasks
    WHEN the token is validated the tasks is created with the data
    THEN return a status code 201 and a json object with the tasks data
    """

    user_id = gen_token["user"]["id"]

    client.set_cookie(
        'refresh_token',
        value=gen_token["tokens"]["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True
    )


    task = {
        "name" : "test_task",
        "status" : False,
        "user_id" : user_id,
    }
    response = client.post('/tasks/',json= task,  headers={"Authorization": f"Bearer {gen_token['tokens']['access_token']}"})

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "test_task"
    assert data["status"] == False
    assert data["user_id"] == user_id

def test_read_task_by_id(client, task_factory):
    data_retrieved = task_factory()
    task_id = data_retrieved["task"]["id"]
    client.set_cookie(
        'refresh_token',
        value=data_retrieved["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True
    )

    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "test_task"
    assert data["status"] == False
    assert data["user_id"] == data_retrieved["task"]["user_id"]

def test_update_task_by_id(client, task_factory):
    data_retrieved = task_factory()
    task_id = data_retrieved["task"]["id"]
    user_id = data_retrieved["task"]["user_id"]
    client.set_cookie(
        'access_token',
        value=data_retrieved["tokens"]["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True
    )

    task = {
        "name": "test_task_updated",
        "status": True,
        "user_id": user_id,
    }

    response = client.put(f'/tasks/{task_id}',json= task, headers={"Authorization": f"Bearer {gen_token['tokens']['access_token']}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "test_task_updated"
    assert data["status"] == True
    assert data["user_id"] == data_retrieved["task"]["user_id"]


def test_delete_task_by_id(client, task_factory):
    data_retrieved = task_factory()
    task_id = data_retrieved["task"]["id"]
    client.set_cookie(
        'access_token',
        value=data_retrieved["access_token"],
        samesite='None',
        httponly=True,
        secure=True
    )

    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == 'Task deleted successfully'
