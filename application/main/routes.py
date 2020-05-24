from flask import request, jsonify
from . import main
from . import client_service

@main.route("/")
def index():
    return "<h1>Hello World!</h1>"

@main.route("/check-username/", methods=["GET"])
def check_username():
    username = request.args.get("username", None)
    print(f"Checking username: {username}")

    response = {}
    if username is None:
        response["ERROR"] = "Missing username necessary for username check."
        return jsonify(response)        
    username_is_available = username.lower() not in client_service.clients
    response["isAvailable"] = username_is_available
    return jsonify(response)

@main.route("/echo")
def returnEcho():
    message = request.args.get("message", None)
    return {
        "echo": message
    }