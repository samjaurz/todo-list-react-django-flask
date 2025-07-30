from flask import Flask
from flask_cors import CORS
from routes.tasks_routes import tasks_api
from routes.users_routes import users_api
app = Flask(__name__)
CORS(app)
app.register_blueprint(tasks_api)
app.register_blueprint(users_api)
@app.route("/")
def hello_world():
    return "<p>Hello!</p>"

if __name__ == "__main__":
    app.run(debug=True)


