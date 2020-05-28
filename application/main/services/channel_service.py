class Channel():
    def __init__(self, id):
        self.id = id

channels = []

def add_dummy_channels():
    for i in range(1, 5):
        channel = Channel(i)
        channels.append(channel)

def get_channels():
    return channels

add_dummy_channels()