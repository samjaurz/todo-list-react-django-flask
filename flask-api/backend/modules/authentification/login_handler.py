import json

class LoginHandler:

    def __init__(
            self,
            event: dict,
            auth,
            user_repository,
            encryption,
            refresh_token_repository
        ):
        self.event = event
        self.auth = auth
        self.user_repository = user_repository
        self._body = None
        self.encryption = encryption
        self.refresh_token_repository = refresh_token_repository

    def login(self):
        user = self.user_repository.get_user_by_email(self.event["email"])
        if not user:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "User not found."
                })
            }
        if user.status is False:
            return {
                "statusCode": 403,
                "body": json.dumps({
                    "message": "User is not authorized.",
                    "user_id": user.id,
                    "email": user.email,
                })
            }

        password_client = self._body["password"]
        password_stored = user.password
        if not self.encryption.checkpw(password_client, password_stored):
            return {
                "statusCode": 401,
                "body": json.dumps({
                    "message": "Invalid password.",
                })
            }
        tokens = self.auth.get_access_token({"user_id": user.id, "email": user.email})

        salt = self.encryption.gensalt()
        refresh_token_prev = tokens["refresh_token"].encode("utf-8")
        refresh_token_hashed = self.encryption.hashpw(refresh_token_prev, salt)
        user_agent = self.event["headers"]["User-Agent"]
        retrieve_refresh_db = self.refresh_token_repository.get_refresh_token_by_user_id(
            user.id
        )

        if retrieve_refresh_db:
            self.refresh_token_repository.update_refresh_token(
                refresh_token_id=retrieve_refresh_db.id,
                **{
                    "token_hash": refresh_token_hashed.decode("utf-8"),
                    "user_agent": user_agent,
                }
            )
        else:
            self.refresh_token_repository.create_refresh_token(
                token_hash=refresh_token_hashed.decode("utf-8"),
                user_agent=user_agent,
                user_id=user.id,
            )

        return {
            "statusCode": 200,
            "body": json.dumps({
                    "message": "Login successful",
                    "user_id": user.id,
                    "access_token": tokens["access_token"]
            })
        }
