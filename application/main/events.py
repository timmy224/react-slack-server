import json
from flask import request
from flask_socketio import emit, join_room, leave_room # didn't add leave_room anywhere yet
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

@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected:")
    room = request.sid
    client_service.remove_client_by_room(room)

### CHALLENGES WEEK 3 ###
@socketio.on("send-ping")
def on_send_ping(message):
    print("Client requested ping:", message)
    response = 'pinged'
    emit("pinged", response, broadcast=True, include_self=True)


@socketio.on("ponged")
def on_pong(message):
    print("Client ponged:", message)
    response = "ping-pong-success"
    emit("ping-pong-success", response, broadcast=True, include_self=True)










    