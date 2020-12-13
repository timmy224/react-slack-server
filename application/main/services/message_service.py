from datetime import datetime
from ...client_models.message import ChannelMessageClient
from ... import db
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from ...models.User import User
from ...models.Channel import Channel
from ...models.Message import Message
from ...models.ChannelMessages import channel_messages
from ...models.PrivateMessages import private_messages
from ...client_models.message import ChannelMessageClient, PrivateMessageClient
from . import channel_service, user_service, org_service, datetime_service
                                                                               
def store_private_message(message):
    org = org_service.get_org(message["org_name"])
    sender = user_service.get_user(message["sender"])
    receiver = user_service.get_user(message["receiver"])
    sent_dt = datetime_service.dt(message["sent_dt"])
    content = message['content']
    message_db = Message(sent_dt, content)
    message_db.sender = sender
    message_db.receiver = receiver    
    message_db.org = org
    db.session.add(message_db)
    db.session.commit()

def store_channel_message(message):
    org = org_service.get_org(message["org_name"])
    sender = user_service.get_user(message["sender"])
    sent_dt = datetime_service.dt(message["sent_dt"])
    content = message['content']
    org_name, channel_name = message["org_name"], message["channel_name"]
    channel = channel_service.get_channel(org_name, channel_name)
    message_db = Message(sent_dt, content)
    message_db.sender = sender
    message_db.channel = channel
    message_db.org = org
    db.session.add(message_db)
    db.session.commit()

def populate_channel_messages_client(messages):
     client_messages = []
     for msg in messages:
         sender, sent_dt, content, channel_id = msg.sender.username, msg.sent_dt, msg.content, msg.channel.channel_id
         sent_dt = datetime_service.string(sent_dt)
         chan_message = ChannelMessageClient(sender, sent_dt, content, channel_id)
         client_messages.append(chan_message)
     client_messages = [chanmsg.__dict__ for chanmsg in client_messages]
     return client_messages

def populate_private_messages_client(messages):
     client_messages = []
     for msg in messages:
         sender, sent_dt, content, receiver = msg.sender.username, msg.sent_dt, msg.content, msg.receiver.username
         sent_dt = datetime_service.string(sent_dt)
         priv_message = PrivateMessageClient(sender, sent_dt, content, receiver)
         client_messages.append(priv_message)
     client_messages = [privmsg.__dict__ for privmsg in client_messages]
     return client_messages

def get_channel_messages(channel, before_date_time):
    base_query =  Message.query\
        .join(channel_messages, Message.message_id == channel_messages.c.message_id)\
        .filter_by(channel_id = channel.channel_id)
    if before_date_time:
        before_dt = datetime_service.dt(before_date_time)
        base_query = base_query.filter(Message.sent_dt < before_dt)
    messages = base_query.order_by(Message.sent_dt.desc()).limit(25).all()
    return messages[::-1]

def get_private_messages(org_name, username1, username2, before_date_time):
    org = org_service.get_org(org_name)
    SendingUser = aliased(User)
    ReceivingUser = aliased(User)
    base_query = Message.query\
        .join(SendingUser)\
        .join(private_messages, Message.message_id==private_messages.c.message_id)\
        .join(ReceivingUser)\
        .filter(or_(\
        ((SendingUser.username==username1) & (ReceivingUser.username==username2)),\
        ((SendingUser.username==username2) & (ReceivingUser.username==username1))\
        ))\
        .filter(Message.org_id==org.org_id)
    if before_date_time:
        before_dt = datetime_service.dt(before_date_time)
        base_query = base_query.filter(Message.sent_dt < before_dt)
    messages = base_query.order_by(Message.sent_dt.desc()).limit(25).all()
    return messages[::-1]