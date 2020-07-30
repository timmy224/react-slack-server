from flask import request, jsonify
from flask_login import login_required
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
        channel_id = channel_service.store_channel(data['channel_name'])

        socketio.emit("channel-created", broadcast=True)
        socketio.emit("added-to-channel", channel_id, broadcast=True)
        response = {}
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


@main.route("/check-channel-name", methods=["POST"])
def check_channel_name():
    data = request.json
    channel_name = data["channel_name"]
    print(f"Checking channel name: {channel_name}")
    name_is_available = db.session.query(Channel.channel_id).filter_by(name=channel_name).scalar() is None
    response = {}
    response['isAvailable'] = name_is_available
    return jsonify(response)

