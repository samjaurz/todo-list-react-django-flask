from backend.flask.auth.auth_jwt import JWTAuth
from flask import request ,jsonify
from functools import wraps

def auth_decorator(func):
    @wraps(func)
    def wrapper(session, **kwargs):
        print("headers",request.headers)
        token = request.headers.get('Authorization').split()[1]
        print("token", token)
        if not token:
            return jsonify({"error": "Token missing"}), 401
        decode = JWTAuth().decode_credentials(token)
        if not decode:
            return jsonify({"error": "This token is invalid"})
        print(decode["user_id"])
        request.user_id = decode["user_id"]
        return func(session,**kwargs)
    return wrapper


