from datetime import datetime
from .channel_service import get_ind_channel, add_message_channel
from .message_class import Message as Message_class
from ... import db
from ...models.User import User
from ...models.Channel import Channel
from ...models.Message import Message as Message_model
from .private_message_service import PrivateMessageClient, MessageClient,ChannelMessageClient

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
    if ChannelMessageClient:
        message = ChannelMessageClient(clientMessage["sender"], 
                      clientMessage["time_sent"], 
                      clientMessage["content"],
                      clientMessage["channel_id"])
    elif PrivateMessageClient:
        message =PrivateMessageClient(clientMessage["sender"], 
                      clientMessage["time_sent"], 
                      clientMessage["content"],
                      clientMessage["receiver"]))
                      
    # message = Message_class(clientMessage["sender"], 
    #                   clientMessage["time_sent"], 
    #                   clientMessage["content"],
    #                   clientMessage["channel_id"]
                      )
    add_message_channel(message, int(clientMessage["channel_id"]))
    #messages.append(message)
                                                                                         
def get_recent_messages(channel_id):
    curr_channel = get_ind_channel(channel_id) 
    return curr_channel.messages[-25:]

def store_private_message(clientMessage):
    """
    Use the User model to query for the person sending and the person receiving.
    Create a new Message model and add the sender and receiver as properties on 
    the Message object. Then add the Message object to the database 
    """
    sender_id = db.session.query(User.user_id).filter_by(username=clientMessage["sender"])
    sent_dt = datetime.strptime(clientMessage["sent_dt"],  "%m/%d/%Y %I:%M %p")
    content = clientMessage['content']
    message = Message_model(sender_id, sent_dt, content)
    
    sender = clientMessage['sender']
    receiver = User.query.filter_by(user_id=clientMessage["receiver"]).one()
    message.receiver = receiver
    
    db.session.add(message)
    db.session.commit()

def store_channel_message(clientMessage):
    sender_id = db.session.query(User.user_id).filter_by(username=clientMessage["sender"])
    sent_dt = datetime.strptime(clientMessage["sent_dt"],  "%m/%d/%Y %I:%M %p")
    content = clientMessage['content']

    sender = clientMessage['sender']
    channel = Channel.query.filter_by(channel_id=clientMessage["channel_id"]).one()
    message = Message_model(sender_id, sent_dt, content)

    message.channel = channel
    
    db.session.add(message)
    db.session.commit()

# add_dummy_messages()
