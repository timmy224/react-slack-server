from .message_service import Message

class Channel():
    def __init__(self, id, name, messages):
        self.id = id
        self.name = name
        self.messages = messages 

channels = {}

def add_dummy_channels():
    for i in range(1, 5):
        channel = Channel(i, f"Channel #{i}", [f"message {i}"])
        channels[i] = channel

def get_channels(): # returns list of available channel ids
    channel_list = [channel for channel in channels]
    return channel_list

def add_channel(createChannel): # have not created socket listener yet
    next_channel = [channel for channel in channels][-1] + 1 # gets most recent channel id + 1
    new_channel = Channel(next_channel, createChannel['name'], []) # create new channel with received name and new id
    channels[next_channel] = new_channel # add new channel instance to channels 

def del_channel(deleteChannel): # have not created socket listener yet
    remove = deleteChannel['id'] # gets id of desired channel to remove
    del channels[remove]

def get_channel_dict(): # just putting it here for possible use later?
    return channels 

def get_ind_channel(channel_id):
    return channels[channel_id]

def add_message_channel(new_message, channel_id):
    channels[channel_id].messages.append(new_message)

def add_dummy_messages():
    for i in range(1, 25):
        username = "user" + str(i+1)
        time_sent = "12:01"
        content = f"My name is {username} and my favorite number is {i+1}"
        dummy_id = 1
        message = Message(username, time_sent, content, dummy_id)
        add_message_channel(message, dummy_id)

add_dummy_channels()
add_dummy_messages()