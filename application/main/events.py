import json
from flask import request
from flask_socketio import emit, join_room, close_room 
from .. import socketio
from .services import client_service
from .services import message_service
import json
from .. import db
from .. models.User import User

@socketio.on("connect")
def on_connect():
    username = request.args.get("username")

    user = User.query.filter_by(username=username)
    channels = user.channel
    rooms_joined = join_room(channel[0].id for channel in channels)

    print(f"Client connected! username: {username}")
    # All clients are assigned a personal room by Flask SocketIO when they connect, named with the session ID of the connection. We want to store this so that we can relay messages to individual clients in the future using send/emit(..., room=room)
    room = request.sid
    client_service.on_client_connected(username, room)
    recent_messages = message_service.get_recent_messages(1) # set default channel here, but removed client socket listener for message-catchup
    recent_messages = json.dumps([message.__dict__ for message in recent_messages])
    emit("message-catchup", recent_messages)
    # Broadcast to all other clients that a new client connected
    emit("user-joined-chat", {"username": username}, broadcast=True, include_self=False)


@socketio.on("send-message")
def on_send_message(clientMessage):
    print("Client sent message")
    print(clientMessage)

    # message_service.on_send_message(clientMessage) - old method
    if clientMessage['type'] == "channel":
        message_service.store_channel_message(clientMessage)
        channel_room = clientMessage['channel_id']
        emit("message-received", clientMessage, room=channel_room, broadcast=True, include_self=True)
    else:
        # insert private message logic here
        pass

# @socketio.on("added-to-channel")
# def on_channel_addition():
#     print("Added to channel:")

#     room = request.sid
#     client_service.remove_client_by_room(room)

@socketio.on("delete-channel")
def on_delete_channel():
    print("Channel deleted:")
    channel_id = request.args.get("channel_id")
    close_room(channel_id)
    emit("Channel deleted", broadcast=True, include_self=True)


@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected:")
    room = request.sid
    client_service.remove_client_by_room(room)


