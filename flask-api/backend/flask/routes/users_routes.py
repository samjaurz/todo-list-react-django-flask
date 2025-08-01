from flask import Blueprint, jsonify, request
from backend.db_session import SessionLocal
from backend.model.users import User
users_api = Blueprint('users_api', __name__)
session = SessionLocal()

@users_api.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        name=data["name"],
        last_name=data["last_name"],
        status=data["status"]
    )
    session.add(user)
    session.commit()
    return jsonify(user.to_dict())


@users_api.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = session.query(User).filter_by(id=id).first()
    if user is None:
        return jsonify({"message": "user not found"})
    return jsonify(user.to_dict())

@users_api.route('/users/', methods=['GET'])
def get_all_users():
    users = session.query(User).order_by(User.id).all()
    if not users:
        return jsonify({"message": "task not found"}), 404
    # todo list comprension
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "last_name": user.last_name,
            "status": user.status
        })
    return jsonify(user_list)

@users_api.route('/users/<int:id>', methods=['PUT'])
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

@users_api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    user = session.query(User).filter_by(id=id).first()
    session.delete(user)
    session.commit()
    return jsonify({"message": "Success"})

@users_api.route('/users/search/', methods=['GET'])
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

@users_api.route('/users/<int:id>/tasks', methods=['GET'])
def get_task_by_user_id(id):
    user = session.query(User).filter_by(id=id).first()
    if user is None:
        return jsonify({"message": "user not found"}), 404
    tasks = user.task
    return jsonify([task.to_dict() for task in tasks])
