from flask import Flask
from flask_cors import CORS
from backend.flask.routes.tasks_routes import tasks_api
from backend.flask.routes.users_routes import users_api
from backend.flask.auth.auth_controller import auth_api
from backend.db_session import SessionFactory
from flasgger import Swagger
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(config_object=None):
    app = Flask(__name__)
    swagger = Swagger(app)

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SUPABASE_DATABASE_URL")

    app.db_factory = SessionFactory(app.config['SQLALCHEMY_DATABASE_URI'])

    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000"],
            "supports_credentials": True,
        }
    })

    app.register_blueprint(tasks_api, url_prefix='/tasks')
    app.register_blueprint(users_api, url_prefix='/users')
    app.register_blueprint(auth_api, url_prefix='/auth')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
