from flask import Blueprint, jsonify, request
from backend.db_session import SessionLocal
from backend.repositories.task_repository import TaskRepository

tasks_api = Blueprint('tasks_api', __name__)
session = SessionLocal()


@tasks_api.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    created_task = TaskRepository(session).create_task(
        name=data["name"],
        status=data["status"],
        user_id=data["user_id"]
    )
    return jsonify(created_task.to_dict()), 200


@tasks_api.route('/<int:id_task>', methods=['GET'])
def get_task_by_id(id_task: int):
    read_task = TaskRepository(session).get_task_by_id(id_task)
    if read_task is None:
        return jsonify({"message": "task not found"})
    return jsonify(read_task.to_dict()), 200


@tasks_api.route('/', methods=['GET'])
def get_task_all():
    tasks = TaskRepository(session).get_all_tasks()
    if not tasks:
        return jsonify({"message": "task not found"}), 404
    return jsonify([task.to_dict() for task in tasks])


@tasks_api.route('/<int:id_task>', methods=['PUT'])
def update_task_by_id(id_task):
    data = request.get_json()
    updated_task = TaskRepository(session).update_task(
        task_id=id_task,
        **{
            "name": data["name"],
            "status": data["status"],
            "user_id": data["user_id"]
        }
    )
    return jsonify({"task_updated": updated_task.to_dict()}), 200


@tasks_api.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    TaskRepository(session).delete_task(task_id)
    return jsonify({"message": "Success"})


@tasks_api.route('/search/', methods=['GET'])
def get_task_by_name():
    name = request.args.get('name')
    if not name:
        tasks = TaskRepository(session).get_all_tasks()
    tasks = TaskRepository(session).get_task_by_name(name)
    return jsonify([task.to_dict() for task in tasks])
