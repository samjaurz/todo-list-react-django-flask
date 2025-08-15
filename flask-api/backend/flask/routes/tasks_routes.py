from flask import Blueprint, jsonify, request
from backend.db_session import with_db_session
from backend.repositories.task_repository import TaskRepository
from backend.flask.auth.decorator import auth_decorator

tasks_api = Blueprint('tasks_api', __name__)

@tasks_api.route('/', methods=['POST'])
@with_db_session
@auth_decorator
def create_task(session):
    data = request.get_json()
    created_task = TaskRepository(session).create_task(
        name=data["name"],
        status=data["status"],
        user_id=data["user_id"]
    )
    return jsonify(created_task.to_dict()), 201


@tasks_api.route('/<int:task_id>', methods=['GET'])
@with_db_session
@auth_decorator
def get_task_by_id(session, task_id: int):
    read_task = TaskRepository(session).get_task_by_id(task_id)
    if read_task is None:
        return jsonify({"message": "task not found"}), 404
    return jsonify(read_task.to_dict()), 200


@tasks_api.route('/<int:task_id>', methods=['PUT'])
@with_db_session
@auth_decorator
def update_task_by_id(session, task_id: int):
    data = request.get_json()
    updated_task = TaskRepository(session).update_task(
        task_id=task_id,
        name=data.get("name"),
        status=data.get("status"),
        user_id=data.get("user_id")
    )
    if not updated_task:
        return jsonify({"message": "Task not found"}), 404
    return jsonify(updated_task.to_dict()), 200


@tasks_api.route('/<int:task_id>', methods=['DELETE'])
@with_db_session
@auth_decorator
def delete_task(session, task_id: int):
    deleted = TaskRepository(session).delete_task(task_id)
    if not deleted:
        return jsonify({"message": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"}), 200

