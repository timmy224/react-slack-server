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
    
