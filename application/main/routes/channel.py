from flask import request, jsonify
import json
from .. import main
from ... import db
from ..services import channel_service
from ...models.User import User, user_schema
from ...models.Channel import Channel, channel_schema

@main.route("/channels/", methods=["GET"])
def get_channels():
    channels = channel_service.get_channel_ids()
    channels_json = json.dumps(channels) # creates JSON string
    response = {}
    response["channels"] = channels_json 
    return response

### DATABASE ROUTES ###

@main.route("/channel/", methods=["GET", "POST"])
def channel():
    if request.method == "GET":
        channel_id = request.args.get("channel_id", None)
        response = {}
        if channel_id is None:
            response["ERROR"] = "Missing channel_id in route"
            return jsonify(response)
        channel = Channel.query.filter_by(channel_id=channel_id).first()
        channel_json = channel_schema.dump(channel)
        response["channel"] = channel_json
        return response        
    elif request.method == "POST":
        data = request.json
        channel = Channel(data["name"])

        db.session.add(channel)
        db.session.commit()

        print("SUCCESS: channel inserted into db")
        response = {}
        response["successful"] = True
        return jsonify(response)

@main.route("/channel-subscription/", methods=["GET", "POST"])
def channel_subscription():
    # Get user's channels (include user_id arg) OR Get channel's users (include channel_id arg)
    if request.method == "GET":
        # Only include one of the following in request url, not both
        user_id = request.args.get("user_id", None)
        channel_id = request.args.get("channel_id", None)
        response = {}
        if user_id is not None: # Going to return this user's channels
            user = User.query.filter_by(user_id=user_id).first()
            channels_json = channel_schema.dump(user.channels, many=True)
            response["channels"] = channels_json
        elif channel_id is not None: # Going to return this channel's users
            channel = Channel.query.filter_by(channel_id=channel_id).first()
            users_json = user_schema.dump(channel.users, many=True)
            response["users"] = users_json
        else:
            response["ERROR"] = "Missing user_id OR channel_id in route (only include one of them)"
        return response

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