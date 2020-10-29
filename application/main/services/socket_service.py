from ... import socketio 

def send(client, event_name, data=None):
    is_connected_client = client is not None
    if is_connected_client: 
        socketio.emit(event_name, data, room=client.room)