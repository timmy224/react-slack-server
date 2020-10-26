from ... import socketio 

def send(client, event_name, data):
    is_connected_client = client is not None
    if is_connected_client: 
        socketio.emit("invited-to-org", org_name, room=client.room)