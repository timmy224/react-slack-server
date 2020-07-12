import json
from flask import request
from flask_socketio import emit, join_room, close_room 
from .. import socketio
from .services import client_service
from .services import message_service
import json
from .. import db
from .. models.User import User

from ..models.Message import Message, MessageSchema, message_schema
from ..models.ChannelMessages import channel_messages

@socketio.on("connect")
def on_connect():
    username = request.args.get("username")

    # user = User.query.filter_by(username=username).first()
    
    # channels = user.channels
    # for channel in channels:
    #     channel_id = channel.channel_id
    #     join_room(channel_id)

    # print(f"Client connected! username: {username}")
    # # All clients are assigned a personal room by Flask SocketIO when they connect, named with the session ID of the connection. We want to store this so that we can relay messages to individual clients in the future using send/emit(..., room=room)
    # room = request.sid
    # client_service.on_client_connected(username, room)

    # # set default channel here, but removed client socket listener for message-catchup
    # # default_channel = 49
    # # recent_messages = Message.query\
    # #                         .join(channel_messages, Message.message_id == channel_messages.c.message_id)\
    # #                         .filter_by(channel_id = default_channel)\
    # #                         .all()
    # # response = {}
    # # response['messages'] = message_schema.dumps(recent_messages, many=True)
    # # print(response)
    # # emit("message-catchup", response)

    # # Broadcast to all other clients that a new client connected
    # emit("user-joined-chat", {"username": username},
    #      broadcast=True, include_self=False)

@socketio.on("send-message")
def on_send_message(clientMessage):
    print("Client sent message")
    print(clientMessage)

    # message_service.on_send_message(clientMessage) - old method
    if clientMessage['type'] == "channel":
        message_service.store_channel_message(clientMessage)
        channel_room = clientMessage['channel_id']
        emit("message-received", clientMessage, room=channel_room, broadcast=True, include_self=True)
    elif clientMessage['type'] == "private":
        message_service.store_private_message(clientMessage)
        receiver_username = clientMessage['receiver']
        receiver_room = client_service.clients[receiver_username].room
        emit("message-recieved", clientMessage, room=receiver_room, broadcast=True, include_self=True)
       

@socketio.on("join-channel")
def on_join_channel(channel_id):
    print("join_channel:", channel_id)
    channel_id = request.args.get("channel_id")
    join_room(channel_id) 

@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected:")
    room = request.sid
    client_service.remove_client_by_room(room)

### Challenge 3
# @socketio.on("ping-test") # for postwoman
# def ping_test(message):
#     emit("pong-test", "hello there", broadcast=True)

@socketio.on("pong-test")
def pong_test():
    emit("ping-pong-success")

@socketio.on("request-ping")
def request_ping(message):
    emit("ping-test")