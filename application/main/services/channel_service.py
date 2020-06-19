from .message_class import Message
from ...models.User import User
from ...models.Channel import Channel as Channel_model
from ... import db
from .message_class import ChannelMessageClient

class Channel():
    def __init__(self, id, name, messages):
        self.id = id
        self.name = name
        self.messages = messages 

channels = {}

def add_dummy_channels():
    for i in range(1, 5):
        channel = Channel(i, f"Channel #{i}", [])
        channels[i] = channel

def get_channel_ids(): # returns list of available channel ids
    return [*channels]

def store_channel(channel_name):
    users = User.query.all()
    name = channel_name
    channel = Channel_model(name)
    channel.users = users

    db.session.add(channel)
    db.session.commit()
    db.session.refresh(channel)
    channel_id = channel.channel_id
    return channel_id

def delete_channel(channel_id):
    channel = Channel_model.query.filter_by(channel_id=channel_id).one()
    channel.users = []

    db.session.commit()
    db.session.delete(channel)
    db.session.commit()

"""

def create_channel(channel_name):
    most_recent_channel_id = [*channels.keys()][-1]
    new_channel_id = most_recent_channel_id + 1

    new_channel = Channel(new_channel_id, channel_name, []) 
    return new_channel

def add_channel(channel): # have not created socket listener yet
    channels[channel["id"]] = channel 

def del_channel(channel_info): # have not created socket listener yet
    remove_id = channel_info['id'] # gets id of desired channel to remove
    del channels[remove_id]

def get_channel_dict(): # just putting it here for possible use later?
    return channels 
"""

def get_ind_channel(channel_id):
    return channels[channel_id]

def add_message_channel(new_message, channel_id):
    channels[channel_id].messages.append(new_message)

def add_dummy_messages():
    for j in range(1, 5):
        dummy_id = j

        for i in range(1, 25):
            username = "user" + str(i+1)
            time_sent = "12:01"
            content = f"Channel #{dummy_id}: My name is {username} and my favorite number is {i+1}"
            message = ChannelMessageClient(username, time_sent, content, dummy_id)
            add_message_channel(message, dummy_id)

add_dummy_channels()
add_dummy_messages()