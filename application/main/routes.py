from datetime import datetime
import json
from flask import request, jsonify
from . import main
from .. import db
from .services import client_service, channel_service, message_service
from ..models.User import User, user_schema
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
        response["ERROR"] = "Missing username in route"
        return jsonify(response)        
    username_is_available = username.lower() not in client_service.clients
    response["isAvailable"] = username_is_available
    return jsonify(response)

@main.route("/channels/", methods=["GET"])
def get_channels():
    channels = channel_service.get_channel_ids()
    channels_json = json.dumps(channels) # creates JSON string
    response = {}
    response["channels"] = channels_json 
    print(response)
    return response
    
"""
def get_channel_dict(): # route to messages
    channels_dict = channel_service.get_channel_dict()
    channels_list_objs = json.dumps([channels_dict[channel].__dict__ for channel in channels_dict])
    response["channels"] = channels_list_objs
    response  = 
        {
            channels: [
                {
                    id: 1,
                    name: "Channel #1",
                    messages: [blah blah blah]
                }, {
                    id: 2,
                    name: "Channel #2",
                    messages: [blah blah blah]
                }, 

                ...

                ]
        }
"""

@main.route("/messages/", methods=["GET"])
def get_channel_messages():
    sel_channel = request.args.get("channelId", None)
    print(f'Received Selected Channel: {sel_channel}')
    sel_channel_messages = message_service.get_recent_messages(int(sel_channel))

    recent_messages = json.dumps([message.__dict__ for message in sel_channel_messages])
    response = {}
    response['messages'] = recent_messages
    print(response)
    return response

### DATABASE ROUTES

# Get / Insert User
@main.route("/user/", methods=["GET", "POST"])
def insert_user():
    if request.method == "GET":
        user_id = request.args.get("user_id", None)
        response = {}
        if user_id is None:
            response["ERROR"] = "Missing user_id in route"
            return jsonify(response)
        user = User.query.filter_by(user_id=user_id).first()

        user = user_schema.dump(user)
        response["user"] = user
        return response
    elif request.method == "POST":
        data = request.json
        user = User(data["username"])

        db.session.add(user)
        db.session.commit()

        print("SUCCESS: user inserted into db")
        response = {}
        response["successful"] = True
        return jsonify(response)

@main.route("/channel", methods=["GET", "POST"])
def insert_channel():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        data = request.json
        channel = Channel(data["name"])

        db.session.add(channel)
        db.session.commit()

        print("SUCCESS: channel inserted into db")
        response = {}
        response["successful"] = True
        return jsonify(response)

@main.route("/channel-subscription", methods=["GET", "POST"])
def insert_channel_subscription():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        data = request.json
        user_id = data["user_id"]
        channel_id = data["channel_id"]
        user = User.query.filter_by(user_id=user_id).first()
        channel = Channel.query.filter_by(channel_id=channel_id).first()

        channel.users.append(user)
        db.session.commit()

        print("SUCCESS: channel_subscription inserted into db")
        response = {}
        response["successful"] = True
        return jsonify(response)
    
@main.route("/private-message", methods=["GET", "POST"])
def insert_private_message():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        data = request.json
        sender_id, content = data["sender_id"], data["content"]
        sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M%p")
        message = Message(sender_id, sent_dt, content)
        receiver = User.query.filter_by(user_id=data["receiver_id"]).first()

        message.receiver = receiver
        db.session.add(message)
        db.session.commit()

        print("SUCCESS: private_message inserted into db")
        response = {}
        response["successful"] = True
        return jsonify(response)

@main.route("/channel-message", methods=["GET", "POST"])
def insert_channel_message():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        data = request.json
        sender_id, content = data["sender_id"], data["content"]
        sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M%p")
        message = Message(sender_id, sent_dt, content)
        channel = Channel.query.filter_by(channel_id=data["channel_id"]).first()

        message.channel = channel
        db.session.add(message)
        db.session.commit()

        print("SUCCESS: channel_message inserted into db")
        response = {}
        response["successful"] = True
        return jsonify(response)


