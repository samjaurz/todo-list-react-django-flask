from flask import Blueprint, jsonify, request
from backend.db_session import with_db_session
from backend.repositories.user_repository import UserRepository
from backend.flask.auth.decorator import auth_decorator
from backend.flask.auth.auth_jwt import JWTAuth
users_api = Blueprint('users_api', __name__)

@users_api.route('/<int:user_id>', methods=['GET'])
@with_db_session
@auth_decorator
def get_user_by_id(session, user_id: int):
    read_user = UserRepository(session).get_user_by_id(user_id)
    if read_user is None:
        return jsonify({"message": "user not found"}), 400
    return jsonify(read_user.to_dict()), 200


@users_api.route('/<int:user_id>/get_tasks', methods=['GET'])
@with_db_session
@auth_decorator
def get_all_task_by_user(session, user_id: int):
    tasks = UserRepository(session).get_all_tasks_by_user(user_id)
    if not tasks:
        return jsonify({
            "user_id": user_id,
            "message": "tasks not found"}) , 404
    return jsonify({
        "user_id":user_id,
        "tasks": tasks
    }), 200

@users_api.route('/search/', methods=['GET'])
@with_db_session
def search_all_task_by_user(session):
    token = request.cookies.get('access_token')
    if not token:
        return jsonify({"error": "Token missing"}), 401
    decode = JWTAuth().decode_credentials(token)
    if not decode:
        return jsonify({"error": "This token is invalid"})

    name = request.args.get('name')

    tasks = UserRepository(session).get_all_tasks_by_user(decode["user_id"])
    filtered_tasks = [task for task in tasks if name.lower() in task['name'].lower()]
    if not tasks:
        return jsonify({
            "user_id": decode["user_id"],
            "message": "tasks not found"}) , 401
    return jsonify({
        "user_id":decode["user_id"],
        "tasks": filtered_tasks
    }), 200
