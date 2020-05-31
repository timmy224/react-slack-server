from datetime import datetime
import json
from flask import request, jsonify
from . import main
from .. import db
from .services import client_service
from .services import channel_service
from ..models.User import User
from ..models.Channel import Channel
from ..models.Message import Message

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

### DATABASE TESTS

# Get / Insert User
@main.route("/user", methods=["GET","POST"])
def insert_user():
    if flask.request.method == "GET":
        pass
    elif flask.request.method == "POST":
        data = request.json
        user = User(data["username"])
        db.session.add(user)
        db.session.commit()
        response = {}
        response["successful"] = True
        return jsonify(response)

@main.route("/channel", methods=["POST"])
def insert_channel():
    data = request.json
    channel = Channel(data["name"])
    db.session.add(channel)
    db.session.commit()
    response = {}
    response["successful"] = True
    return jsonify(response)

@main.route("/channel-subscription", methods=["POST"])
def insert_channel_subscription():
    data = request.json
    user_id = data["user_id"]
    channel_id = data["channel_id"]
    user = User.query.filter_by(user_id=user_id).first()
    channel = Channel.query.filter_by(channel_id=channel_id).first()

    channel.users.append(user)
    db.session.commit()

    response = {}
    response["successful"] = True
    return jsonify(response)
    
@main.route("/private-message", methods=["POST"])
def insert_private_message():
    data = request.json
    sender_id, content = data["sender_id"], data["content"]
    sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M%p")
    message = Message(sender_id, sent_dt, content)
    receiver = User.query.filter_by(user_id=data["receiver_id"]).first()

    message.receiver = receiver
    db.session.add(message)
    db.session.commit()

    response = {}
    response["successful"] = True
    return jsonify(response)

@main.route("/channel-message", methods=["POST"])
def insert_channel_message():
    data = request.json
    sender_id, content = data["sender_id"], data["content"]
    sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M%p")
    message = Message(sender_id, sent_dt, content)
    channel = Channel.query.filter_by(channel_id=data["channel_id"]).first()

    message.channel = channel
    db.session.add(message)
    db.session.commit()

    response = {}
    response["successful"] = True
    return jsonify(response)


