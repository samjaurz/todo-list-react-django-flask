from flask import Blueprint, jsonify, request
from backend.db_session import with_db_session
import bcrypt
from backend.repositories.user_repository import UserRepository
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

    token = JWTAuth().get_access_token({
        "user_id": user.id,
        "email": user.email
    })

    if bcrypt.checkpw(password_client, stored_hash):
        return jsonify({"message": "Password is valid! User authenticated."
                        ,"token": token}), 200
    return jsonify({"error": "Invalid password"}), 401


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
        status=data['status'],
    )
    return jsonify(created_user.to_dict())


