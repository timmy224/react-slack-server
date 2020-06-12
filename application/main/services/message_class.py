class MessageClient():
    def __init__(self, sender, time_sent, content):
        self.sender = sender
        self.time_sent = time_sent
        self.content = content
        
class ChannelMessageClient(MessageClient):
    def __init__(self,channel_id):
        self.channel_id = channel_id

class PrivateMessageClient(MessageClient):
    def __init__(self,receiver):
        self.receiver = receiver