from backend.flask.auth.auth_jwt import JWTAuth
from flask import request, jsonify
from functools import wraps


def auth_decorator(func):
    @wraps(func)
    def wrapper(session, **kwargs):
        headers = request.headers.get("Authorization")
        if not headers:
            return jsonify({"message": "No authorization header"}), 401
        parts = headers.split()
        if len(parts) != 2:
            return jsonify({"message": "Invalid authorization header"}), 401
        if parts[0] != "Bearer":
            return jsonify({"message": "Invalid authorization format"}), 401
        token = headers.split()[1]
        if not token:
            return jsonify({"error": "Token missing"}), 401
        decode = JWTAuth().decode_credentials(token)
        if not decode:
            return jsonify({"error": "This token is invalid"})
        print(decode["user_id"])
        request.user_id = decode["user_id"]
        return func(session, **kwargs)

    return wrapper
