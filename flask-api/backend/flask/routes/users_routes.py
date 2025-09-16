from flask import Blueprint, jsonify, request
from backend.db_session import with_db_session
from backend.repositories.user_repository import UserRepository
from backend.flask.auth.decorator import auth_decorator

users_api = Blueprint("users_api", __name__)


@users_api.route("/<int:user_id>", methods=["GET"])
@with_db_session
@auth_decorator
def get_user_by_id(session, user_id: int):
    """
    Get a user by id
    ---
    tags:
        - Users
    parameters:
        - name: user_id
          in: path
          type: integer
          required: true
          description: ID of the user
        - name: authorization
          in: header
          type: string
          required: true
          description: access token for authentication
    responses:
        200:
         description: User found successfully
         schema:
            type: object
            properties:
                id:
                    type: integer
                name:
                    type: string
                last_name:
                    type: string
                email:
                    type: string
                status:
                    type: boolean
                created_at:
                    type: string
                    format: date-time
                updated_at:
                    type: string
                    format: date-time
        404:
         description: User not found
    """
    read_user = UserRepository(session).get_user_by_id(user_id)
    if read_user is None:
        return jsonify({"message": "User not found"}), 404
    return jsonify(read_user.to_dict()), 200


@users_api.route("/<int:user_id>/tasks", methods=["GET"])
@with_db_session
@auth_decorator
def get_all_task_by_user(session, user_id: int):
    """
    Get all tasks for a user
    ---
    tags:
        - Users
    parameters:
        - name: user_id
          in: path
          type: integer
          required: true
          description: ID of the user
        - name: authorization
          in: header
          type: string
          required: true
          description: access token for authentication
    responses:
        200:
          description: List of tasks found successfully
          schema:
            type: object
            properties:
                id:
                    type: integer
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
         description: User not found
    """
    read_user = UserRepository(session).get_user_by_id(user_id)
    if read_user is None:
        return jsonify({"message": "User not found"}), 404
    tasks = UserRepository(session).get_all_tasks_by_user(user_id)
    return jsonify({"user_id": user_id, "tasks": tasks or []}), 200


@users_api.route("/<int:user_id>/search/", methods=["GET"])
@with_db_session
@auth_decorator
def search_all_task_by_user(session, user_id: int):
    """
    Search the tasks for a specific user
    ---
    tags:
        - Users
    parameters:
        - name: user_id
          in: path
          type: integer
          required: true
          description: ID of the user
        - name: authorization
          in: header
          type: string
          required: true
          description: access token for authentication
        - name: name
          in: query
          type: string
          required: false
          description: query parameter
    responses:
        200:
         description: List of tasks matched with the query successfully
         schema:
            type: object
            properties:
                id:
                    type: integer
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
         description: user not found or task are missing
    """
    read_user = UserRepository(session).get_user_by_id(user_id)
    if read_user is None:
        return jsonify({"message": "User not found"}), 404
    name = request.args.get("name")
    tasks = UserRepository(session).get_all_tasks_by_user(user_id)
    filtered_tasks = [task for task in tasks if name.lower() in task["name"].lower()]
    if not tasks:
        return jsonify({"user_id": user_id, "message": "tasks not found"}), 404
    return jsonify({"user_id": user_id, "tasks": filtered_tasks}), 200
