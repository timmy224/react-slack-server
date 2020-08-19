from flask import request, jsonify
from flask_login import login_required, current_user
import json
from .. import main
from ... import db
from ..services import channel_service
from ...models.Channel import Channel, ChannelSchema
from flask_socketio import close_room
from ... import socketio 

@main.route("/channel", methods=["GET","POST","DELETE"])
# @login_required
def channels():
    if request.method == "GET":
        channels = Channel.query.all()
        channels_json = ChannelSchema(exclude=["users"]).dump(channels, many=True)
        response = {}
        response["channels"] = channels_json
        return response

    elif request.method == "POST":
        data = request.json
        channel_info = data["channel_info"]
        name = channel_info["name"]
        # members = channel_info["members"]
        is_private = channel_info["isPrivate"]
        admin = current_user.username
        # channel_id = channel_service.store_channel(name, members, is_private, admin)
        channel_id = channel_service.store_channel(name, is_private, admin)

        socketio.emit("channel-created", broadcast=True)
        socketio.emit("added-to-channel", channel_id, broadcast=True)
        admin_username = {"channel_username":admin}
        response={}
        response["successful"] = True
        return jsonify(response)

    elif request.method == "DELETE":
        data = request.json
        channel_id = data["channel_id"]
        channel_service.delete_channel(channel_id)
        socketio.close_room(channel_id)

        socketio.emit("channel-deleted", channel_id, broadcast=True)
        response = {}
        response['successful'] = True
        return jsonify(response)


@main.route("/channel/name-available", methods=["POST"])
def check_channel_name():
    data = request.json
    channel_name = data["channel_name"]
    print(f"Checking channel name: {channel_name}")
    name_is_available = db.session.query(Channel.channel_id).filter_by(name=channel_name).scalar() is None
    response = {}
    response['isAvailable'] = name_is_available
    return jsonify(response)



# EXAMPLES #
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
