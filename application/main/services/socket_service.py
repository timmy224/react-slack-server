from ... import socketio
from . import client_service


def send(username, event_name, data=None):
    client = client_service.get_client(username)
    is_connected_client = client is not None
    if is_connected_client:
        socketio.emit(event_name, data, room=client.room)
