from ...models.User import User
from ...models.Channel import Channel as Channel_model
from ... import db
from ...client_models.message import ChannelMessageClient
from sqlalchemy.orm.exc import NoResultFound

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

def get_users_by_usernames(usernames):
    users = []
    usernames_not_found = []
    for username in usernames:
        try:
            user = User.query.filter_by(username=username).one()
            users.append(user)
        except NoResultFound:
            usernames_not_found.append(username)
    return {"users": users, "usernames_not_found": usernames_not_found}

def get_users():
    return User.query.all()

def create_channel(name, members, is_private, admin_username, org):
    channel = Channel_model(name, admin_username, is_private)
    channel.members = members
    channel.org = org
    return channel


def store_channel(channel):
    db.session.add(channel)
    db.session.commit()
    db.session.refresh(channel)
    channel_id = channel.channel_id
    return channel_id

def delete_channel(channel_id):
    channel = Channel_model.query.filter_by(channel_id=channel_id).one()
    channel.members = []

    db.session.commit()
    db.session.delete(channel)
    db.session.commit()

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