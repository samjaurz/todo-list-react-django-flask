from flask import Blueprint, jsonify, request
from backend.model.task import Task
from backend.db_session import SessionLocal
from flask_cors import CORS
api = Blueprint('api', __name__)
CORS(api)
session = SessionLocal()

@api.route('/task/', methods=['POST'])
def create_task():

    data = request.get_json()
    task = Task(
        name=data["name"],
        status=data["status"]
    )
    session.add(task)
    session.commit()

    return jsonify(task.to_dict())

@api.route('/task/<int:id>', methods=['GET'])
def get_task_by_id(id):
    task = session.query(Task).filter_by(id=id).first()
    if task is None:
        return jsonify({"message": "task not found"})
    return jsonify(task.to_dict())

@api.route('/task/', methods=['GET'])
def get_task_all():
    tasks = session.query(Task).order_by(Task.id).all()
    if not tasks:
        return jsonify({"message": "task not found"}) , 404
    #todo list comprension
    task_list = []
    for task in tasks:
        task_list.append({
            "id": task.id,
            "name": task.name,
            "status": task.status
        })
    return jsonify(task_list)

@api.route('/task/<int:id>', methods=['PUT'])
def update_task_by_id(id):
    task = session.query(Task).filter_by(id=id).first()
    if task is None:
        return jsonify({"message": "task not found"}), 404
    required_fields = [
        "name",
        "status"
    ]
    data = request.get_json()
    updated = False

    for key, value in data.items():
        if key in required_fields:
            setattr(task, key, value)
            updated = True
    if updated:
        session.commit()
    return jsonify({"message": "task updated",
                    "task_updated":task.to_dict()}), 200

@api.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = session.query(Task).filter_by(id=id).first()
    session.delete(task)
    session.commit()
    return jsonify({"message": "Success"})

@api.route('/task/search/', methods=['GET'])
def get_task_by_name():
    name = request.args.get('name')
    if not name:
        tasks = session.query(Task).order_by(Task.id).all()
    else:
        tasks = session.query(Task).filter(Task.name.ilike(f"%{name}%")).all()

    task_list = [{
        "id": task.id,
        "name": task.name,
        "status": task.status
    } for task in tasks]

    return jsonify(task_list)

