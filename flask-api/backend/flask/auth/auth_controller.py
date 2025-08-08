
from flask import Blueprint, jsonify, request, current_app
from backend.db_session import SessionLocal
import bcrypt
from backend.repositories.user_repository import UserRepository

auth_api = Blueprint('auth_api', __name__)
session = SessionLocal()

@auth_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    password_client = data['password'].encode('utf-8')

    user = UserRepository(session).get_user_by_email(data['email'])
    if not user:
        return jsonify({"error": "User not found"}), 404

    stored_hash = user.password.encode('utf-8')

    if bcrypt.checkpw(password_client, stored_hash):
        return jsonify({"message": "Password is valid! User authenticated."}), 20
    return jsonify({"error": "Invalid password"}), 401
    # data = request.get_json()
    # password_client = data['password'].encode('utf-8')
    #
    # user = UserRepository(session).get_user_by_email(data['email'])
    # salt, pass_in_db = user.password.split("$_$")
    #
    # salt_b = salt.encode('utf-8')
    # pass_in_db_b = pass_in_db.encode('utf-8')
    # hashed = bcrypt.hashpw(password_client, salt_b)
    #
    # if bcrypt.checkpw(hashed, pass_in_db_b):
    #     return jsonify({"password": "pass"})
    # if hashed == pass_in_db_b:
    #      return jsonify("Password is valid! User authenticated."), 200
    #
    # return jsonify({
    #     "from_db": pass_in_db_b.__str__(),
    #     "from_hashed": hashed.__str__(),
    # }), 401


@auth_api.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    email = UserRepository(session).get_user_by_email(data['email'])
    if data['password'] != data['password_confirmation']:
        return jsonify({"error": "password does not match"})
    if email:
        return jsonify({"error": "email already in use"})

    password_client = data['password'].encode('utf-8')
    salt = bcrypt.gensalt(10)
    hashed = bcrypt.hashpw(password_client, salt)
    created_user = UserRepository(session).create_user(
        name=data['name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed.decode('utf-8'),
        # password=f"{salt.decode('utf-8')}$_${hashed.decode('utf-8')}",
        status=data['status'],
    )
    return jsonify(created_user.to_dict())


