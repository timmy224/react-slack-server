from flask import Blueprint, request, jsonify
import data

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    return "<h1>Hello World!</h1>"

@routes.route("/check-username/", methods=["GET"])
def check_username():
    username = request.args.get("username", None)
    print(f"Checking username: {username}")

    response = {}
    if username is None:
        response["ERROR"] = "Missing username necessary for username check."
        return jsonify(response)        
    username_is_available = username.lower() not in data.socket_connections
    response["isAvailable"] = username_is_available
    return jsonify(response)