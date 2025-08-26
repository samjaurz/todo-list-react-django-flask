from flask import Blueprint, jsonify, request
from backend.db_session import with_db_session
import bcrypt
from backend.repositories.user_repository import UserRepository
from backend.repositories.refresh_token_repository import RefreshTokenRepository
from backend.flask.auth.auth_jwt import JWTAuth
from backend.flask.auth.send_email import EmailSender
auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/login', methods=['POST'])
@with_db_session
def login(session):
    """
    Login user
    ---
    tags:
        - Auth
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
                email:
                    type: string
                password:
                    type: string
    responses:
        200:
            description: Login successful
            schema:
                properties:
                    user_id:
                        type: integer
                    access_token:
                        type: string
        404:
            description: User not found
        403:
            description: User is not verified
        401:
            description: Invalid password
    """
    data = request.get_json()
    password_client = data['password'].encode('utf-8')

    user = UserRepository(session).get_user_by_email(data['email'])
    if not user:
        return jsonify({"message":"User not found"}), 404
    if user.status is False:
        return jsonify({"message": "User is not verified",
                        "user_id": user.id,
                        "email": user.email
                        }),403

    stored_hash = user.password.encode('utf-8')
    if not bcrypt.checkpw(password_client, stored_hash):
        return jsonify({"message": "Invalid password"}), 401

    tokens = JWTAuth().get_access_token({
        "user_id": user.id,
        "email": user.email
    })

    salt = bcrypt.gensalt()
    refresh_token_prev = tokens["refresh_token"].encode('utf-8')
    refresh_token_hashed = bcrypt.hashpw(refresh_token_prev, salt)
    user_agent = request.headers.get('User-Agent', 'Unknown')

    retrieve_refresh_db = RefreshTokenRepository(session).get_refresh_token_by_user_id(user.id)
    if retrieve_refresh_db:
        RefreshTokenRepository(session).update_refresh_token(
            refresh_token_id=retrieve_refresh_db.id,
            **{
                "token_hash": refresh_token_hashed.decode('utf-8'),
                "user_agent": user_agent,
            }
        )
    else:
        RefreshTokenRepository(session).create_refresh_token(
            token_hash=refresh_token_hashed.decode('utf-8'),
            user_agent=user_agent,
            user_id=user.id,
        )
    response = jsonify({"message": "Login successful",
                        "user_id": user.id,
                        "access_token": tokens["access_token"]})
    response.status_code = 200
    response.set_cookie(
        'refresh_token',
        value=tokens["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True,
        max_age=604800,
    )
    return response


@auth_api.route('/sign_up', methods=['POST'])
@with_db_session
def sign_up(session):
    """
    Sign up user
    ---
    tags:
        - Auth
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
                name:
                    type: string
                last_name:
                    type: string
                email:
                    type: string
                password:
                    type: string
                password_confirmation:
                    type: string
            required:
                - name
                - last_name
                - email
                - password
                - password_confirmation
    responses:
            201:
                description: Signup successful
                schema:
                    properties:
                        message:
                            type: string
                        user_id:
                            type: integer
            404:
                description: User not found
            403:
                description: User is not verified
            400:
                description: Email already registered or password is incorrect
    """
    data = request.get_json()
    email = UserRepository(session).get_user_by_email(data['email'])
    if data['password'] != data['password_confirmation']:
        return jsonify({"error": "password does not match"}),401
    if email:
        return jsonify({"error": "email already in use"}),401

    password_client = data['password'].encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_client, salt)
    created_user = UserRepository(session).create_user(
        name=data['name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed.decode('utf-8'),
        status=False,
    )

    tokens = JWTAuth().get_access_token({
        "user_id": created_user.id,
        "email": created_user.email
    })

    refresh_token_prev = tokens["refresh_token"].encode('utf-8')
    refresh_token_hashed = bcrypt.hashpw(refresh_token_prev, salt)
    user_agent = request.headers.get('User-Agent', 'Unknown')

    RefreshTokenRepository(session).create_refresh_token(
        token_hash=refresh_token_hashed.decode('utf-8'),
        user_agent=user_agent,
        user_id=created_user.id,
    )

    EmailSender().send_email(
        to = created_user.email,
        tokens = tokens["access_token"],
    )

    return jsonify({"message": "Sign up successful",
                        "user_id": created_user.id}), 201


@auth_api.route('/logout', methods=['POST'])
def logout():
    """
    Logout user
    ---
    tags:
        - Auth
    responses:
        200:
            description: logout successful
            schema:
                type: object
                properties:
                    message:
                        type: string
        """
    response = jsonify({"message": "Deleted Cookie"})
    response.status_code = 200
    response.delete_cookie(
        'refresh_token',
        httponly=True,
        samesite='None',
        secure=True
    )
    return response


@auth_api.route('/refresh', methods=['GET'])
@with_db_session
def validate_refresh_token(session):
    """
        Generate new access token with th refresh token
        ---
        tags:
            - Auth
        parameters:
            - name: refresh token
              in: cookie
              type: string
              required: true
              description: get refresh token of the cookie

            - name: authorization
              in: header
              type: string
              required: true
              description: access token for authentication
        responses:
                200:
                    description: Generate token successful
                    schema:
                        properties:
                            message:
                                type: string
                            user_id:
                                type: integer
                401:
                    description: Invalid token session expired
        """
    refresh_token = request.cookies.get('refresh_token')
    decode = JWTAuth().decode_credentials(refresh_token)
    if not decode:
        return jsonify({"error": " Invalid token: session expired"}), 401

    tokens = JWTAuth().get_access_token({
        "user_id": decode["user_id"],
        "email": decode["email"]
    })

    retrieve_refresh_db = RefreshTokenRepository(session).get_refresh_token_by_user_id(decode["user_id"])

    salt = bcrypt.gensalt()
    refresh_token_prev = tokens["refresh_token"].encode('utf-8')
    refresh_token_hashed = bcrypt.hashpw(refresh_token_prev, salt)
    user_agent = request.headers.get('User-Agent', 'Unknown')


    RefreshTokenRepository(session).update_refresh_token(
        refresh_token_id=retrieve_refresh_db.id,
        **{
            "token_hash": refresh_token_hashed.decode('utf-8'),
            "user_agent": user_agent,
        }
    )

    response = jsonify({"message": "Generate token successful",
                        "access_token": tokens["access_token"]})
    response.status_code = 200
    response.set_cookie(
        'refresh_token',
        value=tokens["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True,
        max_age=604800,
    )

    return response



@auth_api.route('/verification', methods=['GET'])
@with_db_session
def verification(session):
    """
            Activate the account of the user
            ---
            tags:
                - Auth
            parameters:
                - name: body
                  in: body
                  required: true
                  schema:
                    type: object
                    properties:
                        email:
                            type: string
                    required:
                        - email
                - name: authorization
                  in: header
                  type: string
                  required: true
                  description: access token for authentication
            responses:
                    200:
                        description: Generate token successful
                        schema:
                            properties:
                                message:
                                    type: string
                                user_id:
                                    type: integer
                    401:
                        description: Invalid token session expired
                    404:
                        description: This token is invalid or user not found
            """
    token = request.headers.get('Authorization').split()[1]
    if not token:
        return jsonify({"error": "Token missing"}), 401
    decode = JWTAuth().decode_credentials(token)
    if not decode:
        return jsonify({"error": "This token is invalid"}), 404

    user = UserRepository(session).get_user_by_id(decode["user_id"])
    if not user:
        return jsonify({"error": "User not found"}),404

    UserRepository(session).update_user(
        user_id= decode["user_id"],
        **{
            "status": True
        }
    )

    tokens = JWTAuth().get_access_token({
        "user_id": user.id,
        "email": user.email
    })

    retrieve_refresh_db = RefreshTokenRepository(session).get_refresh_token_by_user_id(user.id)

    salt = bcrypt.gensalt()
    refresh_token_prev = tokens["refresh_token"].encode('utf-8')
    refresh_token_hashed = bcrypt.hashpw(refresh_token_prev, salt)
    user_agent = request.headers.get('User-Agent', 'Unknown')

    RefreshTokenRepository(session).update_refresh_token(
        refresh_token_id=retrieve_refresh_db.id,
        **{
            "token_hash": refresh_token_hashed.decode('utf-8'),
            "user_agent": user_agent,
        }
    )

    response = jsonify({"message": "Verification successful",
                        "access_token": tokens["access_token"]})
    response.status_code = 200
    response.set_cookie(
        'refresh_token',
        value=tokens["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True,
        max_age=604800,
    )

    return response




@auth_api.route('/resend_email_verification', methods=['POST'])
@with_db_session
def resend_email_verification(session):
    print(request)
    data = request.get_json()
    print(data)
    user = UserRepository(session).get_user_by_email(data['email'])
    print(user)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.status:
        return jsonify({"error": "User already verified"}), 402

    tokens = JWTAuth().get_access_token({
        "user_id": user.id,
        "email": user.email
    })

    salt = bcrypt.gensalt()
    refresh_token_prev = tokens["refresh_token"].encode('utf-8')
    refresh_token_hashed = bcrypt.hashpw(refresh_token_prev, salt)
    user_agent = request.headers.get('User-Agent', 'Unknown')

    RefreshTokenRepository(session).create_refresh_token(
        token_hash=refresh_token_hashed.decode('utf-8'),
        user_agent=user_agent,
        user_id=user.id,
    )

    EmailSender().send_email(
        to=user.email,
        tokens=tokens["access_token"],
    )

    return jsonify({"message": "Email sent successfully",
                    "user_id": user.id}), 200


