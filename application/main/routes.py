from flask import request, jsonify
import json
from . import main
from .services import client_service
from .services import channel_service

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

@main.route("/channels/", methods=["GET"])
def get_channels():
    channels = channel_service.get_channels()
    channels = json.dumps([channel.__dict__ for channel in channels])
    response = {}
    response["channels"] = channels
    return response