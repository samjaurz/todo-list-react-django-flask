from flask import Blueprint, jsonify, request
from backend.db_session import SessionLocal
from ..repositories.user_repository import UserRepository
auth_api = Blueprint('auth_api', __name__)
session = SessionLocal()

@auth_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return jsonify({data})

@auth_api.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    email = UserRepository(session).get_user_by_email(data['email'])
    if data['password'] != data['password_confirmation']:
        return jsonify({"error": "password does not match"})
    if email:
        return jsonify({"error": "email already in use"})

    created_user = UserRepository(session).create_user(
        name=data['name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        status=data['status'],
    )
    return jsonify(created_user.to_dict())


