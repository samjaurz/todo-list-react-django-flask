from flask import Blueprint, jsonify, request
from backend.db_session import SessionLocal
from backend.model.user import User
from backend.repositories.user_repository import UserRepository
users_api = Blueprint('users_api', __name__)
session = SessionLocal()

@users_api.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    created_user = UserRepository(session).create_user(
        name=data['name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        status=data['status'],
    )
    return jsonify(created_user.to_dict())

@users_api.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id: int):
    read_user = UserRepository(session).get_user_by_id(user_id)
    if read_user is None:
        return jsonify({"message": "user not found"})
    return jsonify(read_user.to_dict())

@users_api.route('/', methods=['GET'])
def get_all_users():
    users = UserRepository(session).get_all_users()
    if not users:
        return jsonify({"message": "user not found"}), 404
    return jsonify([user.to_dict() for user in users] )

@users_api.route('/<int:id>', methods=['PUT'])
def update_user_by_id(id):
    user = session.query(User).filter_by(id=id).first()
    if user is None:
        return jsonify({"message": "user not found"}), 404
    required_fields = [
        "name",
        "last_name",
        "status"
    ]
    data = request.get_json()
    updated = False

    for key, value in data.items():
        if key in required_fields:
            setattr(user, key, value)
            updated = True
    if updated:
        session.commit()
    return jsonify({"message": "task updated",
                    "task_updated": user.to_dict()}), 200

@users_api.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    UserRepository(session).delete_user(user_id)
    return jsonify({"message": "Success"})

@users_api.route('/search/', methods=['GET'])
def get_user_by_name():
    name = request.args.get('name')
    if not name:
        users = session.query(User).order_by(User.id).all()
    else:
        users = session.query(User).filter(User.name.ilike(f"%{name}%")).all()

    users_list = [{
        "id": user.id,
        "name": user.name,
        "last_name": user.last_name,
        "status": user.status
    } for user in users]

    return jsonify(users_list)

@users_api.route('/<int:user_id>/tasks', methods=['GET'])
def get_task_by_user_id(user_id: int):
    user = UserRepository(session).get_all_tasks_by_user(user_id)
    if not user:
        return jsonify({"message": "user not found"})
    return user
