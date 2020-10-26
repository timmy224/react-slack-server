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
            print(f"Removed {username} from clients")
            del clients[username]
            break

def get_client(username):
    return clients.get(username)

def get_connected_clients(usernames):
    clients = [get_client(username) for username in usernames]
    return filter(lambda client: client is not None, clients)
