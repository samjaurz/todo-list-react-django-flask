from flask import Blueprint, jsonify, request
from backend.db_session import with_db_session
import bcrypt
from backend.repositories.user_repository import UserRepository
from backend.repositories.refresh_token_repository import RefreshTokenRepository

from backend.flask.auth.auth_jwt import JWTAuth

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/login', methods=['POST'])
@with_db_session
def login(session):
    data = request.get_json()
    password_client = data['password'].encode('utf-8')

    user = UserRepository(session).get_user_by_email(data['email'])
    if not user:
        return jsonify({"error": "User not found"}), 404

    stored_hash = user.password.encode('utf-8')
    if not bcrypt.checkpw(password_client, stored_hash):
        return jsonify({"error": "Invalid password"}), 401

    tokens = JWTAuth().get_access_token({
            "user_id": user.id,
            "email": user.email
    })

    response = jsonify({"message": "Login successful",
                        "user_id": user.id,
                        "access_token": tokens["access_token"]})
    response.status_code = 200
    response.set_cookie(
        'refresh_token',
        value=tokens["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True,
        max_age=604800,
    )
    return response


@auth_api.route('/sign_up', methods=['POST'])
@with_db_session
def sign_up(session):
    data = request.get_json()
    email = UserRepository(session).get_user_by_email(data['email'])
    if data['password'] != data['password_confirmation']:
        return jsonify({"error": "password does not match"})
    if email:
        return jsonify({"error": "email already in use"})

    password_client = data['password'].encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_client, salt)
    created_user = UserRepository(session).create_user(
        name=data['name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed.decode('utf-8'),
        status=True,
    )

    tokens = JWTAuth().get_access_token({
        "user_id": created_user.id,
        "email": created_user.email
    })

    response = jsonify({"message": "Sign up successful"})
    response.status_code = 201
    response.headers["Authorization"] = f"Bearer {tokens["access_token"]}"
    response.set_cookie(
        'refresh_token',
        value=tokens["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True,
        max_age=604800,
    )
    return response


@auth_api.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Deleted Cookie"})
    response.status_code = 200
    response.delete_cookie(
        'refresh_token',
        httponly=True,
        samesite='None',
        secure=True
    )
    return response


@auth_api.route('/refresh', methods=['GET'])
@with_db_session
def validate_refresh_token(session):
    print("sdsd")
    refresh_token = request.cookies.get('refresh_token')
    decode = JWTAuth().decode_credentials(refresh_token)
    if not decode:
        return jsonify({"error": " Invalid token: session expired"}), 401

    retrieve_refresh_db =  RefreshTokenRepository(session).get_refresh_token_user_id(decode["user_id"])

    updated_refresh = RefreshTokenRepository(session).update_refresh_token(
    refresh_token_id = retrieve_refresh_db.id,
        **{
            "token_hash": "updated_token_hash",
            "revoked": False,
            "ip_address": "updated_ip_address"
        })

    tokens = JWTAuth().get_access_token({
        "user_id": decode["user_id"],
        "email": decode["email"]
    })



    response = jsonify({"message": "Generate token successful",
                        "access_token": tokens["access_token"]})
    response.status_code = 200
    response.set_cookie(
        'refresh_token',
        value=tokens["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True,
        max_age=604800,
    )

    return response

