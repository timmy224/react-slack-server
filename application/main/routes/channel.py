from flask import request, jsonify
from flask_login import login_required
import json
from .. import main
from ... import db
from ..services import channel_service
from ..services.client_service import clients
from ...models.User import User, user_schema
from ...models.Channel import Channel, ChannelSchema, channel_schema
from sqlalchemy.sql import exists
from flask import request
from flask_socketio import close_room
from ... import socketio 

@login_required
@main.route("/channels/", methods=["GET"])
def get_channels():
    """
    [GET] - Returns a list of server-side stored channels a JSON response
    Path: /channels/
    Response Body: "channels"
    """
    channels = Channel.query.all()
    channels_json = ChannelSchema(exclude=["users"]).dump(channels, many=True)
    response = {}
    response["channels"] = channels_json
    return response

### DATABASE ROUTES ###

### EXAMPLES ###

@main.route("/channel/", methods=["GET", "POST"])
def channel():
    """
    [GET] - Grabs the channel from the DB and returns it as a JSON response
    Path: /channel/?channel_id={channel_id}
    Response Body: "channel"
    
    [POST] - Inserts a channel into the DB using JSON passed in as request body
    Path: /channel/
    Request Body: "name"
    Response Body: "successful"

    DB tables: "channels"
    """
    if request.method == "GET":
        channel_id = request.args.get("channel_id", None)
        response = {}
        if channel_id is None:
            response["ERROR"] = "Missing channel_id in route"
            return jsonify(response)
        channel = Channel.query.filter_by(channel_id=channel_id).one()
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
    """
    IMPORTANT: for GET, only include ONE of the following parameters in the url: "user_id", "channel_id"

    [GET] - If "user_id" route parameter present, grabs the user's channels from the DB and returns it as a JSON response
    If "channel_id" route parameter present, grabs the channel's users from the DB and returns it as a JSON response
    Path: /channel-subscription/?user_id={user_id} OR 
    /channel-subscription/?channel_id={channel_id}
    Response Body: "channels" or "users"
    
    [POST] - Inserts a channel subscription into the DB using JSON passed in as body
    Path: /channel-subscription
    Request Body: "user_id", "channel_id"
    Response Body: "successful"

    DB tables: "users", "channels", "channel-subscriptions"
    """
    # Get user's channels (include user_id arg) OR Get channel's users (include channel_id arg)
    if request.method == "GET":
        # Only include one of the following in request url, not both
        user_id = request.args.get("user_id", None)
        channel_id = request.args.get("channel_id", None)
        response = {}
        if user_id is not None: # Going to return this user's channels
            user = User.query.filter_by(user_id=user_id).one()
            channels_json = channel_schema.dump(user.channels, many=True)
            response["channels"] = channels_json
        elif channel_id is not None: # Going to return this channel's users
            channel = Channel.query.filter_by(channel_id=channel_id).one()
            users_json = user_schema.dump(channel.users, many=True)
            response["users"] = users_json
        else:
            response["ERROR"] = "Missing user_id OR channel_id in route (only include one of them)"
        return response
    elif request.method == "POST":
        data = request.json
        user_id = data["user_id"]
        channel_id = data["channel_id"]
        user = User.query.filter_by(user_id=user_id).one()
        channel = Channel.query.filter_by(channel_id=channel_id).one()

        channel.users.append(user)
        db.session.commit()

        print("SUCCESS: channel_subscription inserted into db")
        response = {}
        response["successful"] = True
        return jsonify(response)

@main.route("/check-channel-name/", methods=['GET'])
def check_channel_name():
    if request.method == "GET":
        channel_name = request.args.get("channel_name", None)
        print(f"Checking channel name: {channel_name}")
        response = {}
        if channel_name is None:
            response["ERROR"] = "Missing channel name in route"
            return jsonify(response)

        exists = db.session.query(db.exists().where(Channel.name == channel_name)).scalar() is not None
        response['isAvailable'] = exists

        return jsonify(response)

print("Client List:", clients)

#possibly split logic for get/post in same route?
@main.route("/create-channel/", methods=['POST'])
def create_channel():
    if request.method == 'POST':
        data = request.json
        channel_id = channel_service.store_channel(data['channel_name'])
        print("SUCCESS: Channel inserted into db")
        
        socketio.emit("channel-created", broadcast=True)
        socketio.emit("added-to-channel", {"channel_id":channel_id}, broadcast=True)
        response = {}
        response["successful"] = True
        return jsonify(response)

@main.route("/delete-channel/", methods=['DELETE'])
def delete_channel():
    if request.method == 'DELETE':
        data = request.json
        channel_id = data["channel_id"]
        channel_service.delete_channel(channel_id)
        socketio.close_room(channel_id)

        print("SUCCESS: Channel deleted from db")
        socketio.emit("channel-deleted", broadcast=True)
        response = {}
        response['successful'] = True
        return jsonify(response)
