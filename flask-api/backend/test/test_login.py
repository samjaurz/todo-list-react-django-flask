import json
from backend.repositories.user_repository import UserRepository
from backend.test.conftest import db_session
from backend.flask.auth.auth_controller import login

def test_login_user(db_session):

    response = login.post(
        '/login', json={
            {"name": "samm",
             "last_name": "jauu",
             "email": "email3@gmail.com",
             "password": "123456",
             "password_confirmation": "123456",
             "status": "true"
             }
        })

    assert response.status_code == 200

    # created_user = UserRepository(db_session).create_user(
    #     name="Samuel",
    #     last_name="Jauregui",
    #     email="samjaurz@gmail.com",
    #     password="1234567",
    #     status=True,
    # )
    #
    # post_event = {
    #     "headers": {
    #         "content-type": "application/json",
    #         "x-api-key": "da2-your-api-key",
    #     },
    #     "requestContext": {
    #         "method": "POST"
    #     },
    #
    #     "body": json.dumps({
    #         "id": created_user.id,
    #         "name": created_user.name,
    #         "email": created_user.email,
    #         "status": created_user.status,
    #         "password": created_user.password,
    #     })
    # }
    # response = login(post_event)