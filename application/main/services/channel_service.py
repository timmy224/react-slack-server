from ...models.User import User
from ...models.Channel import Channel
from ...models.Org import Org
from ... import db
from ...client_models.message import ChannelMessageClient
from sqlalchemy.orm.exc import NoResultFound

def get_channel(org_name, channel_name):
    org = Org.query.filter_by(name=org_name).one()
    channel = next(filter(lambda c: c.name == channel_name, org.channels))
    return channel

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
    channel = Channel(name, admin_username, is_private)
    channel.members = members
    channel.org = org
    return channel

def store_channel(channel):
    db.session.add(channel)
    db.session.commit()
    db.session.refresh(channel)
    channel_id = channel.channel_id
    return channel_id

def delete_channel(channel):
    channel.members = []
    db.session.commit()
    db.session.delete(channel)
    db.session.commit()



