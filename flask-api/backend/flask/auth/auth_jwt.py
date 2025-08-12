import os
import datetime
import jwt


class JWTAuth:
    def __init__(self):
        self.secret = os.getenv("SECRET", "ss")

    def _generate_access_token(self, payload: dict) -> str:
        payload['exp'] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=24)
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def get_access_token(self, payload: dict) -> str:
        return  self._generate_access_token(payload)


    def decode_credentials(self, credentials):
        try:
            return jwt.decode(credentials, key=self.secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return None