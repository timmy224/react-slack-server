from . import socket_service, client_service
from ...models.Channel import channel_schema
from ...client_models.org_member import OrgMemberClient

# ORGS
def send_new_org_member(org_name, username):
    logged_in = True if client_service.get_client(username) else False
    org_member_client = OrgMemberClient(username, logged_in)
    info = {"org_name": org_name, "org_member": org_member_client.__dict__}
    socket_service.send_org(org_name, "new-org-member", info) 

def send_added_to_org(username, org_name):
    socket_service.send_user(username, "added-to-org", org_name)

# ORG MEMBER ONLINE STATUS 
def send_org_member_online(org_name, username):
    info = {"org_name": org_name, "username": username}
    socket_service.send_org(org_name, "org-member-online", info)

def send_org_member_offline(org_name, username):
    info = {"org_name": org_name, "username": username}
    socket_service.send_org(org_name, "org-member-offline", info)

# CHANNELS
def send_added_to_channel(username, channel):
    channel_json = channel_schema.dump(channel)
    info = {"org_name": channel.org.name, "channel": channel_json}
    socket_service.send_user(username, "added-to-channel", info)

def send_channel_deleted(channel):
    org_name, channel_name = channel.org.name, channel.name
    info = {"org_name": org_name, "channel_name": channel_name}
    socket_service.send_channel(org_name, channel_name, "channel-deleted", info)

# MESSAGES
def send_channel_message_received(message):
    org_name, channel_name = message["org_name"], message["channel_name"]
    socket_service.send_channel(org_name, channel_name, "message-received", message)

def send_private_message_received(message):
    receiver_username, sender_username = message["receiver"], message["sender"]
    socket_service.send_user(receiver_username, "message-received", message)
    socket_service.send_user(sender_username, "message-received", message)

# PERMISSIONS
def send_permissions_updated(username):
    socket_service.send_user(username, "permissions-updated")