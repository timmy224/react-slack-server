import collections
from ...models.OrgMemberPermission import org_member_permission_schema
from ...models.ChannelMemberPermission import channel_member_permission_schema
from . import client_service
from ... import socketio 


def gen_org_member_perms_map(org_member_perms):
    """
    Takes in a list of a specific user's OrgMemberPermission and constructs a map with org_id as the key and a list of jsonified OrgMemberPermission as the value
    Returns: the constructed map
    """
    org_to_org_member_perms = collections.defaultdict(list)
    for org_member_perm in org_member_perms:
        org_id = org_member_perm.org_id
        org_member_perm_json = org_member_permission_schema.dump(org_member_perm)
        org_to_org_member_perms[org_id].append(org_member_perm_json)
    return org_to_org_member_perms

def gen_channel_member_perms_map(channel_member_perms):
    """
    Takes in a list of a specific user's ChannelMemberPermission and constructs a nested map with org_id as the top level key
    The value at key org_id is another map, channel_id_to_channel_member_perms. The key is channel_id and
    the value is a list of jsonified ChannelMemberPermission for that Channel
    Returns: the constructed map
    """
    org_to_channel_member_perms = collections.defaultdict(dict)
    for channel_member_perm in channel_member_perms:
        org_id, channel_id = channel_member_perm.org_id, channel_member_perm.channel_id
        channel_id_to_channel_member_perms = org_to_channel_member_perms[org_id]
        if channel_id not in channel_id_to_channel_member_perms:
            channel_id_to_channel_member_perms[channel_id] = []
        channel_member_perm_json = channel_member_permission_schema.dump(channel_member_perm)
        channel_id_to_channel_member_perms[channel_id].append(channel_member_perm_json)
    return org_to_channel_member_perms

def notify_permissions_updated(usernames):    
    """
    Send "permissions-updated" socket event to the subset of usernames that are currently connect clients
    """
    for username in filter(lambda username: client_service.get_client(username) is not None, usernames):
        connected_client = client_service.get_client(username)
        client_room = connected_client.room
        socketio.emit("permissions-updated", room=client_room)


    