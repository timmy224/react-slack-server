from ... import socketio 

def send(client, event_name, data=None):
    is_connected_client = client is not None
    if is_connected_client: 
        socketio.emit("invited-to-org", data, room=client.room)