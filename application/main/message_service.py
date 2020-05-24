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

# Week 1 Challenge
def on_send_special(specialMessage): 
    specialMessageObj = {
        "person": "Special sender",
        "time": "anytime you want =)",
        "message_content": specialMessage
    }

    # adds special message with special sender and time_sent to messages list 
    message = Message(specialMessageObj['person'], specialMessageObj['time'], specialMessageObj['message_content'])
    messages.append(message)

add_dummy_messages()
