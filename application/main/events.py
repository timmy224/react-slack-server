import json
from flask import request
from flask_socketio import emit, join_room, close_room, leave_room
from .. import socketio
from .services import client_service, socket_service, message_service, user_service, event_service, read_status_service
import json
from .. import db
from .. models.User import User
from ..models.Message import Message, MessageSchema, message_schema
from ..models.ChannelMessages import channel_messages


@socketio.on("connect")
def on_connect():
    username = request.args.get("username")
    print(f"Client connected! username: {username}")
    user = user_service.get_user(username)
    channels = user.channels
    for channel in channels:
        org_name = channel.org.name
        room = socket_service.compute_channel_room(org_name, channel.name)
        join_room(room)
    for org in user.orgs:
        room = socket_service.compute_org_room(org.name)
        join_room(room)
        event_service.send_org_member_online(org.name, username)
    room = request.sid
    client_service.on_client_connected(username, room)


@socketio.on("send-message")
def on_send_message(message):
    if message["type"] == "channel":
        message_service.store_channel_message(message)
        event_service.send_channel_message_received(message)
    elif message["type"] == "private":
        message_service.store_private_message(message)
        event_service.send_private_message_received(message)


@socketio.on('leave-channel')
def on_leave_channel(data):
    removed_username = data["removed_username"]
    channel_id = data['channel_id']
    client = client_service.get_client(removed_username)
    sid = client.room
    leave_room(channel_id, sid=sid)
    socket_service.send_user(
            removed_username, "removed-from-channel", data)

@socketio.on('join-channel')
def on_join_channel(info):
    org_name, channel_name = info["org_name"], info["channel_name"]
    room = socket_service.compute_channel_room(org_name, channel_name)
    join_room(room)


@socketio.on("join-org")
def on_join_org(org_name):
    room = socket_service.compute_org_room(org_name)
    join_room(room)


@socketio.on("disconnect")
def on_disconnect():
    room = request.sid
    username = client_service.get_username_by_room(room)
    if username: 
        print("Client disconnected:", username)
        client_service.remove_client_by_room(room)
        user = user_service.get_user(username)
        for org in user.orgs:
            event_service.send_org_member_offline(org.name, username)

@socketio.on("read_status")
def on_read_status(read_status):
    """ updates private or channel read status """
    username = client_service.get_username_by_room(room)
    if read_status["type"] == "private":
        read_status_service.set_read_status_private(read_status)
    elif read_status["type"] == "channel":
        read_status_service.set_read_status_channel(read_status)
    # TODO revisit refactoring set_read_(...)_status functions (take in second param)