from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

socket_connections = {"codeninja", None}
messages = []

@app.route("/")
def index():
    return "<h1>Hello World!</h1>"

@app.route("/check-username/", methods=["GET"])
def check_username():
    username = request.args.get("username", None)
    print(f"Checking username: {username}")

    response = {}
    if username is None:
        response["ERROR"] = "Missing username necessary for username check."
        return jsonify(response)        
    username_is_available = username.lower() not in socket_connections
    response["isAvailable"] = username_is_available
    return jsonify(response)

# if __name__ == "__main__":
#     socketio.run(app)


