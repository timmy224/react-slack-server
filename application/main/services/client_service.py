from collections import namedtuple
Client = namedtuple("Client", ["username", "room"])

clients = {}

def on_client_connected(username, room):
    add_client(username, room)

def add_client(username, room):
    clients[username] = Client(username, room)
    
def remove_client_by_room(room):
    for username, client in list(clients.items()):
        if client.room == room:
            del clients[username]
            break

def get_client(username):
    return clients.get(username)

def get_connected_clients(usernames):
    connected_clients = []
    for username in usernames:
        client = get_client(username)
        if client is not None:
            connected_clients.append(client)
    return connected_clients

def get_username_by_room(room):
    for client in clients.values():
        if client.room == room:
            return client.username


