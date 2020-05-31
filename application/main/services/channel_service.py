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

def get_channels():
    channel_list = [channel for channel in channels]
    return channel_list

def get_channel_dict(): # just putting it here for possible use later?
    return channels 

def add_channel(createChannel): # have not created socket listener yet
    next_channel = [channel for channel in channels][-1] + 1 # gets most recent channel id + 1
    new_channel = Channel(next_channel, createChannel['name'], []) # create new channel with received name and new id
    channels[next_channel] = new_channel # add new channel instance to channels 

def del_channel(deleteChannel): # have not created socket listener yet
    remove = deleteChannel['id'] # gets id of desired channel to remove
    del channels[remove]

add_dummy_channels()