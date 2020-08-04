from collections import namedtuple
Client = namedtuple("Client", ["username", "room"])

clients = {}

def add_dummy_clients():
    add_client("codeninja", None)
    add_client("hacker", None)
    add_client("bitboy", None)

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

add_dummy_clients()