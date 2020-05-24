import json
from flask import request
from flask_socketio import emit
from .. import socketio
from . import client_service
from . import message_service
import json

@socketio.on("connect")
def on_connect():
    username = request.args.get("username")
    print(f"Client connected! username: {username}")
    # All clients are assigned a personal room by Flask SocketIO when they connect, named with the session ID of the connection. We want to store this so that we can relay messages to individual clients in the future using send/emit(..., room=room)
    room = request.sid
    client_service.on_client_connected(username, room)
    recent_messages = message_service.get_recent_messages()
    recent_messages = json.dumps([message.__dict__ for message in recent_messages])
    emit("message-catchup", recent_messages)
    # Broadcast to all other clients that a new client connected
    emit("user-joined-chat", {"username": username}, broadcast=True, include_self=False)

@socketio.on("send-message")
def on_send_message(clientMessage):
    print("Client sent message")
    print(clientMessage)
    message_service.on_send_message(clientMessage)
    emit("message-received", clientMessage, broadcast=True, include_self=True)
    print("After send")

@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected:")
    room = request.sid
    client_service.remove_client_by_room(room)

@socketio.on("my-special-event") # challenge 2 and 3 
def on_special_event(specialMessage):
    print(specialMessage)
    message_service.on_send_special(specialMessage)
    emit("special-message-received", specialMessage, broadcast=True, include_self=True)