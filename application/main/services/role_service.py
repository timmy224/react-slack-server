from sqlalchemy import and_
from ...models.Role import Role
from ...models.ChannelMembers import channel_members
from ... import db

def get_role(name):
    role = Role.query.filter_by(name=name).one()
    return role

def gen_channel_members_role_update(channel_id, member_ids, role_id):
    statement = channel_members.update().where(
        and_(
            channel_members.c.channel_id == channel_id,
            channel_members.c.user_id.in_(member_ids)
        )
    ).values(role_id=role_id)
    return statement

