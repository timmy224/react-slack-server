import collections
from ...models.OrgMemberPermission import OrgMemberPermission, org_member_permission_schema
from ...models.ChannelMemberPermission import ChannelMemberPermission, channel_member_permission_schema
from . import client_service, socket_service
from ... import db

def get_org_member_perms(username):
    """
    Queries for a user's org member permissions and returns a permissions map with org_name as the key
    """
    org_member_perms = db.session.query(OrgMemberPermission).filter_by(username=username).all()
    return gen_org_member_perms_map(org_member_perms)

def get_channel_member_perms(username):
    """
    Queries for a user's org member permissions and returns a permissions map with org_name as the top level key and channel name as the second level key 
    """
    channel_member_perms = db.session.query(ChannelMemberPermission).filter_by(username=username).all()
    return gen_channel_member_perms_map(channel_member_perms)

def gen_org_member_perms_map(org_member_perms):
    """
    Takes in a list of a specific user's OrgMemberPermission and constructs a map with org_name as the key and a list of jsonified OrgMemberPermission as the value
    Returns: the constructed map
    """
    org_to_org_member_perms = collections.defaultdict(list)
    for org_member_perm in org_member_perms:
        org_name = org_member_perm.org_name
        org_member_perm_json = org_member_permission_schema.dump(org_member_perm)
        org_to_org_member_perms[org_name].append(org_member_perm_json)
    return org_to_org_member_perms


def gen_channel_member_perms_map(channel_member_perms):
    """
    Takes in a list of a specific user's ChannelMemberPermission and constructs a nested map with org_name as the top level key
    The value at key org_name is another map, channel_name_to_channel_member_perms. The key is channel_name and
    the value is a list of jsonified ChannelMemberPermission for that Channel
    Returns: the constructed map
    """
    org_to_channel_member_perms = collections.defaultdict(dict)
    for channel_member_perm in channel_member_perms:
        org_name, channel_name = channel_member_perm.org_name, channel_member_perm.channel_name
        channel_name_to_channel_member_perms = org_to_channel_member_perms[org_name]
        if channel_name not in channel_name_to_channel_member_perms:
            channel_name_to_channel_member_perms[channel_name] = []
        channel_member_perm_json = channel_member_permission_schema.dump(channel_member_perm)
        channel_name_to_channel_member_perms[channel_name].append(
            channel_member_perm_json)
    return org_to_channel_member_perms
