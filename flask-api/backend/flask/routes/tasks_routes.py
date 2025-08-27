from flask import Blueprint, jsonify, request
from backend.db_session import with_db_session
from backend.repositories.task_repository import TaskRepository
from backend.flask.auth.decorator import auth_decorator

tasks_api = Blueprint('tasks_api', __name__)


@tasks_api.route('/', methods=['POST'])
@with_db_session
@auth_decorator
def create_task(session):
    """
    Create a new task
    ---
    tags:
        - Task
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
                name:
                    type: string
                status:
                    type: boolean
                user_id:
                    type: integer
          description: a payload of the required fields to create the task
        - name: authorization
          in: header
          type: string
          required: true
          description: access token for authentication
    responses:
        200:
         description: Task created
         schema:
          properties:
            name:
                type: string
            status:
                type: boolean
            user_id:
                type: integer
    """
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
    """
    Get a task by id
    ---
    tags:
        - Task
    parameters:
        - name: task_id
          in: path
          type: integer
          required: true
          description: ID of the task
        - name: authorization
          in: header
          type: string
          required: true
          description: access token for authentication
    responses:
        200:
         description: Task found
         schema:
                type: object
                properties:
                    task:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: integer
                                status:
                                    type: boolean
                                user_id:
                                    type: integer
        404:
         description: task not found
    """
    read_task = TaskRepository(session).get_task_by_id(task_id)
    if read_task is None:
        return jsonify({"message": "task not found"}), 404
    return jsonify(read_task.to_dict()), 200


@tasks_api.route('/<int:task_id>', methods=['PUT'])
@with_db_session
@auth_decorator
def update_task_by_id(session, task_id: int):
    """
    Update a task
    ---
    tags:
        - Task
    parameters:
        - name: task_id
          in: path
          type: integer
          required: true
          description: ID of the task
        - name: authorization
          in: header
          type: string
          required: true
          description: access token for authentication

    responses:
        200:
         description: Task updated successfully
         schema:
                type: object
                properties:
                    task:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: integer
                                status:
                                    type: boolean
                                user_id:
                                    type: integer
        404:
         description: task not found
    """
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
    """
    Delete a task
    ---
    tags:
        - Task
    parameters:
            - name: task_id
              in: path
              type: integer
              required: true
              description: ID of the task
            - name: authorization
              in: header
              type: string
              required: true
              description: access token for authentication
    responses:
            200:
             description: Task deleted successfully
             schema:
                type: object
                properties:
                    message:
                        type: string

            404:
                description: Task not found
    """
    deleted = TaskRepository(session).delete_task(task_id)
    if not deleted:
        return jsonify({"message": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"}), 200
