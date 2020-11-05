from sqlalchemy import and_
from ... import db
from ...models.Role import Role
from ...models.ChannelMembers import channel_members
from ...models.OrgMembers import org_members

def get_role(name):
    role = Role.query.filter_by(name=name).one()
    return role

def gen_channel_members_role_update_by_member_ids(channel_id, member_ids, role_id):
    statement = channel_members.update().where(
        and_(
            channel_members.c.channel_id == channel_id,
            channel_members.c.user_id.in_(member_ids)
        )
    ).values(role_id=role_id)
    return statement

def gen_channel_members_role_update_by_channel_ids(channel_ids, member_id, role_id):
    statement = channel_members.update().where(
        and_(
            channel_members.c.channel_id.in_(channel_ids),
            channel_members.c.user_id == member_id
        )
    ).values(role_id=role_id)
    return statement

def gen_org_members_role_update(org_id, member_id, role_id):
    statement = org_members.update().where(
        and_(
            org_members.c.org_id == org_id,
            org_members.c.user_id == member_id
        )
    ).values(role_id=role_id)
    return statement



