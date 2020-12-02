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

def get_users_channels(user, org_name):
    return list(filter(lambda channel: channel.org.name == org_name, user.channels))

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

def populate_channel_client(channel):
    channels_json = channel_schema.dump(org.channels, many=True)
    members = []
    for member in org.members:
        logged_in = True if client_service.get_client(member.username) else False
        org_member_client = OrgMemberClient(member.username, logged_in)
        members.append(org_member_client.__dict__)
    return OrgClient(org.name, members).__dict__

def is_channel_name_available(org, channel_name):
    return not any(channel.name == channel_name for channel in org.channels)
