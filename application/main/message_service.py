from collections import namedtuple
from datetime import datetime
Message = namedtuple("Message", ["sender", "time_sent", "content"]) 
messages = []

def add_dummy_messages():
    for i in range(1, 25):
        username = "user" + str(i+1)
        time_sent = "12:01"
        content = f"My name is {username} and my favorite number is {i+1}"
        message = Message(username, time_sent, content)
        messages.append(message)

def on_send_message(clientMessage):
    message = Message(clientMessage["sender"], clientMessage["time_sent"], clientMessage["content"])
    messages.append(message)
                                                                                                                        
def get_recent_messages():
    return messages[-25:]

add_dummy_messages()
