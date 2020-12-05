from ... import socketio
from . import client_service

def compute_org_room(org_name):
    return org_name

def compute_channel_room(org_name, channel_name):
    return f"{org_name}:{channel_name}"

def send_user(username, event_name, data=None):
    client = client_service.get_client(username)
    is_connected_client = client is not None
    if is_connected_client:
        send_room(client.room, event_name, data)

def send_channel(org_name, channel_name, event_name, data=None):
    room = compute_channel_room(org_name, channel_name)
    send_room(room, event_name, data)

def send_org(org_name, event_name, data=None):
    send_room(org_name, event_name, data)

def send_room(room, event_name, data=None):
    socketio.emit(event_name, data, room=room)
    
def close_channel_room(org_name, channel_name):
    room = compute_channel_room(org_name, channel_name)
    socketio.close_room(room)

