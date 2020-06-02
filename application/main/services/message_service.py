from datetime import datetime
from .channel_service import get_ind_channel, add_message_channel
from .message_class import Message
# class Message():
#     def __init__(self, sender, time_sent, content, channel_id):
#         self.sender = sender
#         self.time_sent = time_sent
#         self.content = content
#         self.channel_id = channel_id

#messages = []

# def add_dummy_messages():
#     for i in range(1, 25):
#         username = "user" + str(i+1)
#         time_sent = "12:01"
#         content = f"My name is {username} and my favorite number is {i+1}"
#         dummy_id = 1
#         message = Message(username, time_sent, content, dummy_id)
#         add_message_channel(message, dummy_id)
        #messages.append(message)

def on_send_message(clientMessage):
    message = Message(clientMessage["sender"], 
                      clientMessage["time_sent"], 
                      clientMessage["content"],
                      clientMessage["channel_id"]
                      )
    add_message_channel(message, int(clientMessage["channel_id"]))
    #messages.append(message)
                                                                                         
def get_recent_messages(channel_id):
    curr_channel = get_ind_channel(channel_id) 
    
    print(curr_channel.messages[-25:])
    return curr_channel.messages[-25:]

# add_dummy_messages()
