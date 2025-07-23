from flask import Flask
from api_endpoints import api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(api)
@app.route("/")
def hello_world():
    return "<p>Hello!</p>"

if __name__ == "__main__":
    app.run(debug=True)


