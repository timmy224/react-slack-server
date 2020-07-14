from datetime import datetime
from .channel_service import get_ind_channel, add_message_channel
from .message_class import ChannelMessageClient
from ... import db
from ...models.User import User
from ...models.Channel import Channel
from ...models.Message import Message as Message_model
from ..services.message_class import ChannelMessageClient, PrivateMessageClient

messages = []

def add_dummy_messages():
    for i in range(1, 25):
        username = "user" + str(i+1)
        time_sent = "12:01"
        content = f"My name is {username} and my favorite number is {i+1}"
        dummy_id = 1
        message = ChannelMessageClient(username, time_sent, content, dummy_id)
        add_message_channel(message, dummy_id)
        messages.append(message)

def on_send_message(clientMessage):
    message = ChannelMessageClient(clientMessage["sender"], 
                      clientMessage["time_sent"], 
                      clientMessage["content"],
                      clientMessage["channel_id"]
                      )
    add_message_channel(message, int(clientMessage["channel_id"]))
    messages.append(message)                                                                                   

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

add_dummy_messages()
def pop_channel_messages_client(messages):
     chan_message = None
     chan_messages_client= []
     for msg in messages:
         sender= msg.sender.username
         sent_dt= msg.sent_dt
         content= msg.content
         channel_id= msg.channel.channel_id

         chan_message= ChannelMessageClient(sender, sent_dt, content, channel_id)
         chan_messages_client.append(chan_message)
     chan_messages_list = [chanmsg.__dict__ for chanmsg in chan_messages_client]
     return chan_messages_list

def pop_private_messages_client(messages):
     priv_message = None
     priv_messages_client=[]
     for msg in messages:
         sender= msg.sender.username
         sent_dt= msg.sent_dt
         content= msg.content
         receiver= msg.receiver.username

         priv_message= PrivateMessageClient(sender, sent_dt, content, receiver)
         priv_messages_client.append(priv_message)
     priv_messages_list = [privmsg.__dict__ for privmsg in priv_messages_client]
     return priv_messages_list
