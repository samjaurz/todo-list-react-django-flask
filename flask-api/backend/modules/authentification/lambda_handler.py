from backend.modules.authentification.login_handler import LoginHandler
from backend.flask.auth.auth_jwt import JWTAuth
from backend.repositories.user_repository import UserRepository
from backend.repositories.refresh_token_repository import RefreshTokenRepository

import bcrypt
def lambda_handler(event, context):
    request_context = event["requestContext"]
    resource_path = request_context.get("resourcePath", "")
    method = request_context.get("method")
    auth = JWTAuth()
    user_repository = UserRepository(event["db_session"])
    refresh_token_repository = RefreshTokenRepository(event["db_session"])

    encryption = bcrypt

    if method == "POST":
        if resource_path == "/product/":
            return LoginHandler(
                event=event,
                auth=auth,
                encryption=encryption,
                user_repository=user_repository,
                refresh_token_repository = refresh_token_repository,
            ).login()

