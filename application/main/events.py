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
    user = db.session.query(User.user_id).filter_by(username={username})
    channels_joined = user.channels
    print(f"Client connected! username: {username}")
    # All clients are assigned a personal room by Flask SocketIO when they connect, named with the session ID of the connection. We want to store this so that we can relay messages to individual clients in the future using send/emit(..., room=room)
    room = request.sid
    client_service.on_client_connected(username, room)
    recent_messages = message_service.get_recent_messages(1) # set default channel here, but removed client socket listener for message-catchup
    recent_messages = json.dumps([message.__dict__ for message in recent_messages])
    emit("message-catchup", recent_messages)
    # Broadcast to all other clients that a new client connected
    emit("user-joined-chat", {"username": username}, broadcast=True, include_self=False)
'''
**on socket connection**

When a client connects, use the user_id to look up the channels to which 
that user belongs using a SQLAlchemy query. If you query using the User model, 
the channels will be available as a property on the user object. 

Now that you can get at that channels, we're going to make the user join one 
socket-io room for each channel, where the room is the channel_id. 

join_room(channel1.id)
join_room(channel2.id)
join_room(channel3.id)
'''
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