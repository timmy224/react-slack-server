from datetime import datetime

class Message():
    def __init__(self, sender, time_sent, content):
        self.sender = sender
        self.time_sent = time_sent
        self.content = content

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

#basically defining the form for the special message and its contents/available information
def on_send_special_message(specialMessage):
    specialMessageObj = {
        "sender":"Special sender",
        "time": "now",
        "message_content": specialMessage
    }
message=Message(specialMessageObj['sender'], specialMessageObj['time'], specialmessageObj['message_content'])
#this adds this special message to the list of messages
messages.append(message)
