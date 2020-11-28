from . import socket_service
from ...models.Channel import channel_schema

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