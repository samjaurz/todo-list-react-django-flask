
from flask import Blueprint, jsonify, request
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
    salt, pass_in_db = user.password.split("$_$")

    salt_b = bytes(salt)
    hashed = bcrypt.hashpw(password_client, salt_b)


    if bcrypt.checkpw(pass_in_db, hashed):
         return jsonify("Password is valid! User authenticated.")
    return jsonify({
        "from_db": pass_in_db.__str__(),
        "from_hashed": hashed.__str__(),
    })


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
        password=f"{salt}$_${hashed}",
        status=data['status'],
    )
    return jsonify(created_user.to_dict())


