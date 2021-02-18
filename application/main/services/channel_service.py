from ...models.User import User
from ...models.Channel import Channel
from ...models.Org import Org
from ... import db
from ...client_models.message import ChannelMessageClient
from sqlalchemy.orm.exc import NoResultFound
from ..services import role_service
from ...constants.roles import channel_roles


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


def delete_channel_user(channel, username):
    member = User.query.filter_by(username=username).one()
    channel.members.remove(member)
    db.session.commit()


def add_channel_member(channel, new_member):
    channel.members.append(new_member)
    db.session.commit()


def set_channel_member_role(channel_id, user):
    members_channel_role = role_service.get_role(
        channel_roles.TADPOLE)
    statement = role_service.gen_channel_member_role_update_by_member_id(
        channel_id, user.user_id, members_channel_role.role_id)
    db.session.execute(statement)
    db.session.commit()

# def add_dummy_messages():
#     for j in range(1, 5):
#         dummy_id = j

#         for i in range(1, 25):
#             username = "user" + str(i+1)
#             time_sent = "12:01"
#             content = f"Channel #{dummy_id}: My name is {username} and my favorite number is {i+1}"
#             message = ChannelMessageClient(
#                 username, time_sent, content, dummy_id)
#             add_message_channel(message, dummy_id)


# add_dummy_channels()
# add_dummy_messages()


def populate_channel_client(channel):
    channels_json = channel_schema.dump(org.channels, many=True)
    members = []
    for member in org.members:
        logged_in = True if client_service.get_client(
            member.username) else False
        org_member_client = OrgMemberClient(member.username, logged_in)
        members.append(org_member_client.__dict__)
    return OrgClient(org.name, members).__dict__


def is_channel_name_available(org, channel_name):
    return not any(channel.name == channel_name for channel in org.channels)
