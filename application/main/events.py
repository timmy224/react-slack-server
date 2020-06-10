import json
from flask import request
# didn't add leave_room anywhere yet
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from .services import client_service
from .services import message_service
import json


@socketio.on("connect")
def on_connect():
    username = request.args.get("username")
    print(f"Client connected! username: {username}")
    # All clients are assigned a personal room by Flask SocketIO when they connect, named with the session ID of the connection. We want to store this so that we can relay messages to individual clients in the future using send/emit(..., room=room)
    room = request.sid
    client_service.on_client_connected(username, room)
    # set default channel here, but removed client socket listener for message-catchup
    recent_messages = message_service.get_recent_messages(1)
    recent_messages = json.dumps(
        [message.__dict__ for message in recent_messages])
    emit("message-catchup", recent_messages)
    # Broadcast to all other clients that a new client connected
    emit("user-joined-chat", {"username": username},
         broadcast=True, include_self=False)


@socketio.on("send-message")
def on_send_message(clientMessage):
    print("Client sent message")
    print(clientMessage)

    # message_service.on_send_message(clientMessage) - old method
    if clientMessage['type'] == "channel":
        message_service.store_channel_message(clientMessage)
        channel_room = clientMessage['channel_id']
        emit("message-received", clientMessage,
             room=channel_room, broadcast=True, include_self=True)

        # where the socket handles the private messages for storing and sending.
    elif clientMessage['type'] == "private":
        message_service.store_private_message(clientMessage)
        receiver_username = clientMessage['username']
        receiver_room = client_service.clients[receiver_username].room
        emit("message-recieved", clientMessage,
             room=receiver_room, broadcast=True, include_self=True)

    print("After send")


@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected:")
    room = request.sid
    client_service.remove_client_by_room(room)
