from flask import request, jsonify
import json
from . import main
from .services import client_service
from .services import channel_service
from .services import message_service

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
    print()
    print()

    recent_messages = json.dumps([message.__dict__ for message in sel_channel_messages])
    response = {}
    response['messages'] = recent_messages
    print(response)
    return response
    