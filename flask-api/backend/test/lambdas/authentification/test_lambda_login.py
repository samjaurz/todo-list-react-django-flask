import json
from backend.modules.authentification.lambda_handler import lambda_handler


def test_lambda_login(db_session, admin_user_factory):
    user = admin_user_factory(
         status=True,
     )

    post_event = {
        "headers": {
            "content-type": "application/json",
            "x-api-key": "da2-your-api-key"
        },
        "requestContext": {
            "resourcePath": "/login",
            "method": "POST"
        },

        "db_session": db_session,
        "body": json.dumps({
                "email": "test_account@email.com",
                "password": 12345678
            })
    }

    response = lambda_handler(post_event, "")
    assert response["statusCode"] == 200