from backend.flask.auth.auth_jwt import JWTAuth
from flask import request ,jsonify
from functools import wraps

def auth_decorator(func):
    @wraps(func)
    def wrapper(session, **kwargs):
        token = request.cookies.get('access_token')
        if not token:
            return jsonify({"error": "Token missing"}), 401
        decode = JWTAuth().decode_credentials(token)
        if not decode:
            return jsonify({"error": "This token is invalid"})
        return func(session,**kwargs)
    return wrapper

