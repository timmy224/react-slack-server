from flask_socketio import emit
from __main__ import socketio

socket_connections = {"codeninja", None}
messages = []

@socketio.on("connect")
def on_connect():
    print("Client connected!")
    emit("connect-response", {"data": "connected"})

@socketio.on("message")
def on_message(message):
    print("Client sent message")
    print(message)
    emit("message-received", {"data": "received message"})

@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected!")
